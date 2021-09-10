
// char* fgets(char* str, int num, FILE* stream);
Interceptor.attach(Module.getExportByName(null, 'fgets'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.str     = args[0];
    this.num     = args[1].toInt32();
    this.stream  = args[2];
  },
  onLeave: function (result) {
    console.log("fets: ");
    if (this.num > 0) {
      send(hexdump(this.str, { length: this.num, ansi: false }));
    }
  }
})
