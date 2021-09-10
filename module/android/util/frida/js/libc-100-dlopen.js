
// void *dlopen(const char *filename, int flag);
Interceptor.attach(Module.getExportByName(null, 'dlopen'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.filename     = args[0];
    this.flag         = args[1].toInt32();
  },
  onLeave: function (result) {
    var addr = result;

    send('dlopenName : ' + this.filename);
  }
})
