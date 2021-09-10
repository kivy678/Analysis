
console.log("[*] Start Script");

Java.perform(function () {
    
    Java.enumerateLoadedClasses({
      onMatch: function (name, handle) {
        if (name == 'sg.vantagepoint.uncrackable2'){
            console.log(name);
        };

      },

      onComplete: function () {
        console.log('complete');
      }

    });


});

console.log("[*] End Script");
