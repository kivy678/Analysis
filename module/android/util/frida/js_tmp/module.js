
console.log("[*] Start Script");

Java.perform(function() {
	
    console.log("[*] start Hook");

    var libc = Module.load('libfoo.so');
    var addr = null;

    libc.enumerateImports().forEach(function(element) {
        //console.log(element.name);
        if (element.name == 'strncmp') {
            console.log("[*] strncmp: ", element.address);
            addr = element.address;
        };
    });


    var results = Memory.scanSync(libc.base, libc.size, '7f 45 4c 46');
    console.log('Memory.scanSync() result:\n' + JSON.stringify(results));


    Memory.protect(libc.base, 4096, 'rw-');


    console.log(hexdump(libc.base, {
        offset: 0,
        length: 128,
        header: true,
        ansi: true
    }));  

    Memory.patchCode(libc.base, 64, function (code) {   // 사이즈는 64
    var cw = new X86Writer(code);
        cw.putMovRegU32('eax', 9000);
        cw.putRet();
        cw.flush();                   // 데이터를 메모리에 씀. 항상 호출해주는 것이 좋다.
    });

    console.log(hexdump(libc.base, {
        offset: 0,
        length: 128,
        header: true,
        ansi: true
    }));


    console.log("[*] end Hook");
});


console.log("[*] End Script");

