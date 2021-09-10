
// void *dlsym(void *handle, const char *symbol);
Interceptor.attach(Module.getExportByName(null, 'dlsym'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.handle     = args[0];
    this.symbol     = args[1];
  },
  onLeave: function (result) {
    var addr = result;

    send('dlsymName : ' + this.symbol);
    send('dlsymAddr : ' + addr);
  }
})
