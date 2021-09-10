
console.log("[*] Start Script");

Java.perform(function() {
	
    console.log("[*] start Hook");

    var libc = Module.findBaseAddress('libfoo.so');

    console.log(hexdump(libc, {
    	offset: 0,
    	length: 128,
    	header: true,
    	ansi: true

    }));

    Process.enumerateRanges('rwx').forEach(function(element) {
    console.log(element.base); })
    
    Process.enumerateModules().forEach(function(element) {
       console.log(element.name); })
    
    
});


console.log("[*] End Script");

