// Load in node_repl after importing @oai/sky. One observed action per call.
// This guarded replacement addresses the later EMPTY-A02 closure association error.
// A new run is required for every new evidence attempt.
globalThis.r2Action = async function (label, x, y, key, scroll) {
  const ctx = globalThis.r2Context;
  if (!ctx?.state || !ctx.root) throw Error('Select and observe the current run first');
  const fs = await import('node:fs/promises');
  const manifest = JSON.parse(await fs.readFile(ctx.root + '/manifest.json', 'utf8'));
  const facts = JSON.parse(await fs.readFile(ctx.root + '/observer/window.json', 'utf8'));
  if (facts.playerPid !== manifest.pid || facts.hwnd !== ctx.state.window.id ||
      !facts.foregroundVerified || facts.foregroundPid !== manifest.pid || facts.hwndPid !== manifest.pid)
    throw Error('Run, HWND and foreground identity must agree before logging or input');
  const observation = ctx.state, shot = observation.screenshots[0];
  const beforeText = await fs.readFile(ctx.root + '/observer/state.json', 'utf8').catch(() => null);
  const before = beforeText ? JSON.parse(beforeText) : null;
  const record = {step: ++ctx.step, label, utc: new Date().toISOString(), window: facts,
    screenshot: {id: shot.id, originX: shot.originX, originY: shot.originY, width: shot.width, height: shot.height},
    screenshotPoint: {x, y},
    clientPoint: {x: shot.originX + x - facts.clientOriginScreen.x, y: shot.originY + y - facts.clientOriginScreen.y},
    screenPoint: {x: shot.originX + x, y: shot.originY + y}, before};
  await fs.appendFile(ctx.root + '/actions.jsonl', JSON.stringify(record) + '\n');
  ctx.state = null;
  if (key) await sky.press_key({window: observation.window, key});
  else if (scroll) await sky.scroll({window: observation.window, screenshotId: shot.id, x, y, scrollY: scroll, scrollX: 0});
  else await sky.click({window: observation.window, screenshotId: shot.id, x, y});
  ctx.state = await sky.get_window_state({window: observation.window});
  await new Promise(resolve => setTimeout(resolve, 250));
  const after = JSON.parse(await fs.readFile(ctx.root + '/observer/state.json', 'utf8'));
  await fs.appendFile(ctx.root + '/outcomes.jsonl', JSON.stringify({step: record.step, label, utc: new Date().toISOString(), after}) + '\n');
};
