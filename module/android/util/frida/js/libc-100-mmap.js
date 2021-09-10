
// void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
Interceptor.attach(Module.getExportByName(null, 'mmap'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.addr     = args[0];
    this.length   = args[1].toInt32();
    this.prot     = args[2].toInt32();
    this.flags    = args[3].toInt32();
    this.fd       = args[4].toInt32();
    this.offset   = args[5].toInt32();
  },
  onLeave: function (result) {
    var addr = result;

    send('mmapAddr   : ' + addr);
    send('mmaplength : ' + this.length);
  }
})
