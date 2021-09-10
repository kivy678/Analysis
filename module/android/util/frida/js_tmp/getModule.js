
console.log("[*] Start Script");

Java.perform(function() {
	
  console.log("[*] start Hook");
  try {
  	var linker_addr = null;
  	var linker_size = null;

    Process.enumerateModules().forEach(function(element) {
        if (element.name == 'linker') {
            console.log("[*] Module Name: ", element.name);
            linker_addr = element.base;				// native pointer
            linker_size = element.size;
        };
	})

		//var m = new NativePointer(addr);
		//console.log(m);

	linker_addr.enumerateImports().forEach(function(element) {
	  //console.log(element.name);
	  //if (element.name == 'strncmp') {
	  //    console.log("[*] strncmp: ", element.address);
	  //    addr = element.address;
	  //};
	});

		//var results = Memory.scanSync(linker_addr, linker_size, 'c6 44 24 5f');
		//console.log('Memory.scanSync() result:\n' + JSON.stringify(results));

  } catch (e) {
  	console.log(e.name, e.message);
  }


    console.log("[*] end Hook");
});


console.log("[*] End Script");
