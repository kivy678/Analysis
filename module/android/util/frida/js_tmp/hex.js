
console.log("[*] Start Script");
    var add_array = [
    "0xb7ca1857",
    "0xb41a33ea",
    "0xa3b11ddd",
    "0xb41a48bb",
    "0xb7d2a8c1",
    "0xb7d2a4e5",
    "0xb7d9efd7",
    "0xb7d9f0d1",
    "0xaf8af757",
    "0xa3b11a3d",
    "0xa3af7227",
    "0xa3b1596b"
]

    add_array.forEach(function(item, index, array){
    var m = new NativePointer(item);

        console.log(hexdump(m, {
            offset: 0,
            length: 16,
            header: true,
            ansi: true
        }));

    

    })




console.log("[*] End Script");

