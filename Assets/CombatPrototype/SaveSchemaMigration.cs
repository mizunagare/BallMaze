using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Xml;
using System.Xml.Linq;
using UnityEngine;

// v10 is a separate writable collection. The v9 client never selects this path.
internal static class SaveSchemaMigration
{
#if UX_ACCEPTANCE
    internal static Action<string, string> MigrationValidationHook;
    static void ObserveMigration(string phase, string path) => MigrationValidationHook?.Invoke(phase, path);
#endif
    internal const int Version = 10;
    internal static string Target(string v9) => Path.GetFullPath(v9) + "-v10";

    internal static FileStream Acquire(string root)
    {
        root = Path.GetFullPath(root);
        string lockPath = root + ".v10.lock";
        ValidationStorage.RejectLinks(root);
        ValidationStorage.RejectLinks(lockPath);
        Directory.CreateDirectory(Path.GetDirectoryName(root));
        return new FileStream(lockPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None);
    }

    internal static string Generation(string root)
    {
        return FingerprintFile(Path.Combine(root, "save.json")) + ":" +
            FingerprintFile(Path.Combine(root, "save.json.bak"));
    }

    internal static string FingerprintFile(string path)
    {
        ValidationStorage.RejectLinks(path);
        if (!File.Exists(path)) return "missing";
        using (var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read | FileShare.Delete))
        using (var sha = System.Security.Cryptography.SHA256.Create())
            return BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "");
    }

    internal static void WriteBytes(string path, byte[] bytes)
    {
        using (var stream = new FileStream(path, FileMode.CreateNew, FileAccess.Write, FileShare.None))
        {
            stream.Write(bytes, 0, bytes.Length);
            stream.Flush(true);
        }
    }

    internal static byte[] Encode(CombatSaveData data, int version)
    {
        var payload = JsonUtility.ToJson(data);
        var envelope = new CombatSaveEnvelope
        {
            version = version, revision = data.revision, savedAtUtc = ObjectiveHistoryEntry.UtcNow(),
            payload = payload, checksum = SaveCatalog.Hash(Encoding.UTF8.GetBytes(payload))
        };
        var bytes = Encoding.UTF8.GetBytes(JsonUtility.ToJson(envelope, true));
        if (bytes.Length > 8 * 1024 * 1024) throw new IOException("主存档超过读取预算");
        return bytes;
    }

    internal static void VerifyHistoryWire(string payload, CombatSaveData data)
    {
        // JsonUtility treats missing bools as false and ignores unknown fields.
        // Check the approved wire contract independently before trusting those defaults.
        using (var reader = JsonReaderWriterFactory.CreateJsonReader(Encoding.UTF8.GetBytes(payload),
            new XmlDictionaryReaderQuotas { MaxDepth = 128, MaxStringContentLength = 8 * 1024 * 1024,
                MaxArrayLength = 200000, MaxBytesPerRead = 65536, MaxNameTableCharCount = 32768 }))
        {
            var root = XElement.Load(reader);
            VerifyProfileWire(One(root, "profile", "object"));
            if (data.hasSettlement) VerifyProfileWire(One(One(root, "settlement", "object"), "plan", "object"));
        }
    }

    static XElement One(XElement node, string name, string type)
    {
        var values = node.Elements(name).ToArray();
        if (values.Length != 1 || (string)values[0].Attribute("type") != type)
            throw new InvalidDataException("目标历史字段缺失或类型非法：" + name);
        return values[0];
    }

    static readonly string[] EntryKeys =
        { "runId", "objectiveId", "regionId", "completedAtUtc", "committedAtUtc", "displayNameSnapshot" };

    static void VerifyProfileWire(XElement profile)
    {
        One(profile, "objectiveHistoryLegacyUnknown", "boolean");
        foreach (var item in One(profile, "objectiveHistory", "array").Elements())
        {
            if ((string)item.Attribute("type") != "object" || item.Elements().Count() != EntryKeys.Length)
                throw new InvalidDataException("目标历史项结构非法");
            foreach (var key in EntryKeys) One(item, key, "string");
        }
    }

    [Serializable] sealed class Entry { public string path, sha256; public long bytes; }
    [Serializable] sealed class Manifest { public int sourceVersion = 9; public string sourceFingerprint; public Entry[] files; }

    static IEnumerable<string> Files(string path)
    {
        ValidationStorage.RejectLinks(path);
        foreach (var entry in Directory.EnumerateFileSystemEntries(path).OrderBy(p => p, StringComparer.Ordinal))
        {
            ValidationStorage.RejectLinks(entry);
            if (Directory.Exists(entry))
            {
                foreach (var file in Files(entry)) yield return file;
            }
            else yield return entry;
        }
    }

    static Entry[] SourceEntries(string source)
    {
        var files = Files(source).Select(path => Describe(path, "collection/" + Relative(source, path))).ToList();
        foreach (string extension in new[] { ".newgame.json", ".newgame.json.tmp" })
        {
            var file = source + extension;
            if (File.Exists(file)) files.Add(Describe(file, "associated/transaction" + extension));
        }
        // An unresolved directory transition needs the old client's explicit recovery.
        if (files.Any(e => e.path.StartsWith("associated/", StringComparison.Ordinal)))
        {
            var journal = source + ".newgame.json";
            if (!File.Exists(journal) || File.Exists(journal + ".tmp") || !NewGameJournalFinal(journal))
                throw new IOException("v9 新档事务未确认。请先在旧客户端完成恢复");
        }
        var parent = Path.GetDirectoryName(source);
        var name = Path.GetFileName(source);
        foreach (var folder in Directory.EnumerateDirectories(parent).OrderBy(p => p, StringComparer.Ordinal))
        {
            var leaf = Path.GetFileName(folder);
            if (leaf.StartsWith(name + ".archive-", StringComparison.OrdinalIgnoreCase) ||
                leaf.StartsWith(name + ".newgame-", StringComparison.OrdinalIgnoreCase) ||
                leaf.StartsWith(name + ".migration-staging", StringComparison.OrdinalIgnoreCase))
                files.AddRange(Files(folder).Select(path => Describe(path, "associated/" + leaf + "/" + Relative(folder, path))));
        }
        return files.OrderBy(e => e.path, StringComparer.Ordinal).ToArray();
    }

    [Serializable] sealed class JournalPhase { public string phase; }

    static bool NewGameJournalFinal(string file)
    {
        ValidationStorage.RejectLinks(file);
        var phase = JsonUtility.FromJson<JournalPhase>(File.ReadAllText(file))?.phase;
        return phase == "committed" || phase == "aborted";
    }

    static string Relative(string root, string path) =>
        path.Substring(root.Length + 1).Replace(Path.DirectorySeparatorChar, '/');

    static Entry Describe(string path, string relative) =>
        new Entry { path = relative, sha256 = FingerprintFile(path), bytes = new FileInfo(path).Length };

    static string OriginalPath(string source, string relative)
    {
        const string transaction = "associated/transaction";
        if (relative.StartsWith(transaction, StringComparison.Ordinal)) return source + relative.Substring(transaction.Length);
        if (relative.StartsWith("collection/", StringComparison.Ordinal)) return Path.Combine(source, relative.Substring(11));
        return Path.Combine(Path.GetDirectoryName(source), relative.Substring(11));
    }

    static void CopyVerified(string source, string destination, Entry expected)
    {
        ValidationStorage.RejectLinks(source);
        Directory.CreateDirectory(Path.GetDirectoryName(destination));
        using (var input = new FileStream(source, FileMode.Open, FileAccess.Read, FileShare.Read | FileShare.Delete))
        using (var output = new FileStream(destination, FileMode.CreateNew, FileAccess.Write, FileShare.None))
        {
            input.CopyTo(output);
            output.Flush(true);
        }
        VerifyFile(destination, expected);
    }

    static void VerifyFile(string path, Entry expected)
    {
        if (FingerprintFile(path) != expected.sha256 || new FileInfo(path).Length != expected.bytes)
            throw new IOException("快照文件校验失败：" + expected.path);
    }

    internal static void ImportV9(string source, string target, string expectedSource)
    {
        source = Path.GetFullPath(source);
        target = Path.GetFullPath(target);
        if (target == source || !target.EndsWith("-v10", StringComparison.OrdinalIgnoreCase))
            throw new IOException("v10 必须使用独立存档根");
        ValidationStorage.Record("v10-import-source", source);
        ValidationStorage.Record("v10-import-target", target);
        using (Acquire(target))
        {
            if (Directory.Exists(target) || File.Exists(target))
                throw new IOException("目标集合已经存在，保留原样");
            if (SaveCatalog.Fingerprint(source) != expectedSource)
                throw new IOException("v9 源档已变化，请重新检查");
#if UX_ACCEPTANCE
            ObserveMigration("before-archive", source);
#endif
            var entries = SourceEntries(source);
            var manifest = new Manifest { files = entries };
            manifest.sourceFingerprint = SaveCatalog.Hash(Encoding.UTF8.GetBytes(JsonUtility.ToJson(manifest)));
            // Keep intermediate paths below the Windows Mono length limit. The archive
            // name is a locator; the full manifest and every file are still checked.
            string parent = Path.GetDirectoryName(target);
            string archive = target + ".before-v10-" + manifest.sourceFingerprint.Substring(0, 16);
            bool archived = Directory.Exists(archive);
            string backupStage = archived ? archive : Path.Combine(parent, ".ux05-b-" + Guid.NewGuid().ToString("N").Substring(0, 12));
            string manifestPath = Path.Combine(backupStage, "manifest.json");
            if (archived && File.ReadAllText(manifestPath) != JsonUtility.ToJson(manifest, true))
                throw new IOException("既有原档备份清单不匹配");
            foreach (var e in entries)
            {
                string destination = Path.Combine(backupStage, e.path);
                if (archived) VerifyFile(destination, e);
                else CopyVerified(OriginalPath(source, e.path), destination, e);
            }
            var after = SourceEntries(source);
            if (SaveCatalog.Fingerprint(source) != expectedSource ||
                JsonUtility.ToJson(new Manifest { files = after }) != JsonUtility.ToJson(new Manifest { files = entries }))
                throw new IOException("复制期间 v9 源档发生变化，请重新检查");
            if (!archived)
            {
                WriteBytes(manifestPath, Encoding.UTF8.GetBytes(JsonUtility.ToJson(manifest, true)));
                Directory.Move(backupStage, archive);
            }

            string snapshot = Path.Combine(archive, "collection");
            string primary = Path.Combine(snapshot, "save.json");
            CombatSaveData data = null;
            if (File.Exists(primary))
            {
                try { data = CombatSaveSystem.InspectReadOnly(primary); }
                catch (InvalidDataException) { } // Selection falls back only to the complete verified old backup.
                catch (ArgumentException) { } // JsonUtility reports malformed JSON with ArgumentException.
            }
            if (data == null && File.Exists(primary + ".bak")) data = CombatSaveSystem.InspectReadOnly(primary + ".bak");
            if (data == null || data.sourceVersion != 9) throw new IOException("未找到完整可读的 v9 存档");

            data.profile.objectiveHistory = Array.Empty<ObjectiveHistoryEntry>();
            data.profile.objectiveHistoryLegacyUnknown = true;
            if (data.hasSettlement)
            {
                data.settlement.plan.objectiveHistory = Array.Empty<ObjectiveHistoryEntry>();
                data.settlement.plan.objectiveHistoryLegacyUnknown = true;
            }
            checked { data.revision++; }
            AdventureValidation.Validate(data, true, Version);
            string stage = Path.Combine(parent, ".ux05-p-" + Guid.NewGuid().ToString("N").Substring(0, 12));
            Directory.CreateDirectory(stage);
            GroundLootStore.Pack(data, stage);
            var bytes = Encode(data, Version);
            var stagePrimary = Path.Combine(stage, "save.json");
#if UX_ACCEPTANCE
            ObserveMigration("before-candidate-write", stagePrimary);
#endif
            WriteBytes(stagePrimary, bytes);
            WriteBytes(Path.Combine(stage, "v10-migration.json"), Encoding.UTF8.GetBytes(JsonUtility.ToJson(manifest, true)));
#if UX_ACCEPTANCE
            ObserveMigration("candidate-ready", stagePrimary);
#endif
            VerifyCandidate(stagePrimary, bytes, data);
            if (Directory.Exists(target) || File.Exists(target)) throw new IOException("发布前目标集合改变");
#if UX_ACCEPTANCE
            ObserveMigration("before-replace", stagePrimary);
#endif
            Directory.Move(stage, target);
#if UX_ACCEPTANCE
            ObserveMigration("after-replace", Path.Combine(target, "save.json"));
#endif
            VerifyCandidate(Path.Combine(target, "save.json"), bytes, data);
        }
    }

    static void VerifyCandidate(string path, byte[] bytes, CombatSaveData expected)
    {
        var actual = CombatSaveSystem.InspectReadOnly(path);
        if (FingerprintFile(path) != SaveCatalog.Hash(bytes) || actual.sourceVersion != Version ||
            actual.revision != expected.revision || actual.profile.profileId != expected.profile.profileId)
            throw new IOException("v10 持久化回读不匹配");
    }
}
