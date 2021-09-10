
// int sendto(int s, const void *msg, size_t len, int flags, const struct sockaddr *to, socklen_t tolen); 
Interceptor.attach(Module.getExportByName(null, 'sendto'), {
  onEnter: function (args) {
    //console.log('Context  : '   + JSON.stringify(this.context));
    //console.log('ReturnAddr : ' + this.returnAddress);

    this.fd     = args[0].toInt32();
    this.msg    = args[1];
    this.len    = args[2].toInt32();
    this.flags  = args[3].toInt32();
    this.to     = args[4];
    this.tolen  = args[5].toInt32();
  },
  onLeave: function (result) {
    var numBytes = result.toInt32();

    if (numBytes > 0) {
      send(hexdump(this.msg, { length: numBytes, ansi: false }));
    }

    send('SendToCount   : ' + numBytes);
  }
})
