
console.log("[*] Start Script");

Java.perform(function() {
	
    console.log("[*] start Hook");

    var m = new NativePointer('0xb77c2000');
    console.log(m);


    var results = Memory.scanSync(libc.base, libc.size, '7f 45 4c 46');
    console.log('Memory.scanSync() result:\n' + JSON.stringify(results));


    console.log("[*] end Hook");
});


console.log("[*] End Script");
