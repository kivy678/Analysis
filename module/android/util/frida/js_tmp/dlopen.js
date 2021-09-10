
console.log("[*] Start Script");


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

