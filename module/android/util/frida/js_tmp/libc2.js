
console.log("[*] Start Script");

var hModule = Process.findModuleByName("libc++.so");
var base_addr = hModule.base;

//console.log(base_addr.add(0xABCDEF).readPointer()); // 0x0 in console

MemoryAccessMonitor.enable(
    {
        base: base_addr,
        size: 8 // qword
    },
    {
        onAccess: function(details) {
            console.log(
                "operation: " + details.operation + 
                " from: " + details.from.sub(base_addr) + 
                " address: " + details.address
            );
        }
    }
);

Interceptor.attach(base_addr, {
    onLeave: function(retval) {
        console.log(base_addr); // value in console
    }
});

var dlopen = new NativeFunction(Module.findExportByName(null, 'dlopen'), 'pointer', ['pointer', 'int']);

Interceptor.replace(dlopen, new NativeCallback(function(path, mode) {
    console.log("dlopen(" + "path=\"" + Memory.readUtf8String(path) + "\"" + ", mode=" + mode + ")");
    var name = Memory.readUtf8String(path);
    if (name !== null) {
        console.log("[*] dlopen " + name);
    }
    return dlopen(path, mode);
}, 'pointer', ['pointer', 'int']));


console.log("[*] End Script");

