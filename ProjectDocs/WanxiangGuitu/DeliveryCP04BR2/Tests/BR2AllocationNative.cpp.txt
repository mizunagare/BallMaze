// Test-only Mono profiler bridge. No managed callback or heap allocation in Allocation().
typedef unsigned long long U64;
extern "C" __declspec(dllimport) void* __stdcall GetModuleHandleW(const wchar_t*);
extern "C" __declspec(dllimport) void* __stdcall GetProcAddress(void*,const char*);
typedef void* (__cdecl *Create)(void*);typedef int (__cdecl *Enable)();typedef unsigned int (__cdecl *Size)(void*);typedef void (__cdecl *Callback)(void*,void*);typedef void (__cdecl *Set)(void*,Callback);
static void* handle;static Set set;static Size size;static int available,enableResult;static int marker;
static __declspec(thread) int active,busy;static __declspec(thread) U64 bytes,count,invalid;
static void __cdecl Allocation(void*,void* object){if(!active||busy)return;busy=1;unsigned int n=size(object);if(n>0&&n<0x40000000){bytes+=n;count++;}else invalid++;busy=0;}
extern "C" __declspec(dllexport) int BR2Init(){void* m=GetModuleHandleW(L"mono-2.0-bdwgc.dll");if(!m)return -1;Create create=(Create)GetProcAddress(m,"mono_profiler_create");Enable enable=(Enable)GetProcAddress(m,"mono_profiler_enable_allocations");set=(Set)GetProcAddress(m,"mono_profiler_set_gc_allocation_callback");size=(Size)GetProcAddress(m,"mono_object_get_size");if(!create||!enable||!set||!size)return -2;handle=create(&marker);if(!handle)return -3;set(handle,Allocation);available=1;enableResult=enable();return enableResult;}
extern "C" __declspec(dllexport) void BR2Begin(){bytes=count=invalid=0;active=available;}
extern "C" __declspec(dllexport) void BR2End(U64* b,U64* c,U64* i){active=0;*b=bytes;*c=count;*i=invalid;}
extern "C" __declspec(dllexport) void BR2Stop(){active=0;if(handle&&set)set(handle,0);}
