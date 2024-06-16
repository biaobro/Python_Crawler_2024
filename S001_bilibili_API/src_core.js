// core.sj
// CURRENT_FNVAL cookie 里的名称是全大写。直接搜是搜不到的
t.prototype.injectFnVal = function() {
    var e = y.a.getFnVal({
        mseSupported: this.mseSupported,
        enableHEVC: this.enableHEVC,
        enableAV1: this.enableAV1
    });
    S.a.set(h.o, e.toString())
}

t.getFnVal = function(e) {
    var t = 1;
    return e && e.mseSupported && (t = 16,
    e.enableHEVC && (t = 2e3),
    e.enableAV1 && (t = 4048)),
    t
}

// log-reporter.js
// b_lsid
x = function(x) {
    var e = this.splitDate()
      , t = Object(f.b)(e.millisecond)
      , t = "".concat(Object(f.c)(8), "_").concat(t);
    this.lsid = t,
    this.time.start = e.millisecond,
    this.time.day = e.day,
    c.a.setCookie("b_lsid", t, 0, "current-domain")
}
e = function(e) {
    var t = new Date(e || Date.now())
      , n = t.getDate()
      , r = t.getHours()
      , e = t.getMinutes()
      , t = t.getTime();
    return {
        day: n,
        hour: r,
        minute: e,
        second: Math.floor(t / 1e3),
        millisecond: t
    }
}
o = function(e) {
    return Math.ceil(e).toString(16).toUpperCase()
}

// e 固定为8
// 8次循环，不代表得到8位，数字16 经过转换会得到2位 10
// 极端情况下，8次循环可能会得到16位数字：1010101010101010
// 因为存在向上取整
a = function(e) {
    for (var t = "", n = 0; n < e; n++)
        t += o(16 * Math.random());
    return s(t, e)
}

// e 是得到的随机字符串，t还是固定为8
// 如果长度小于8，就补0
// 什么情况下会得到长度小于8 的字符串 e？
s = function(e, t) {
    var n = "";
    if (e.length < t)
        for (var r = 0; r < t - e.length; r++)
            n += "0";
    return n + e
}


// uuid
var r = function() {
    var e = a(8)
      , t = a(4)
      , n = a(4)
      , r = a(4)
      , o = a(12)
      , i = (new Date).getTime();
    return e + "-" + t + "-" + n + "-" + r + "-" + o + s((i % 1e5).toString(), 5) + "infoc"
}
  , a = function(e) {
    for (var t = "", n = 0; n < e; n++)
        t += o(16 * Math.random());
    return s(t, e)
}
  , s = function(e, t) {
    var n = "";
    if (e.length < t)
        for (var r = 0; r < t - e.length; r++)
            n += "0";
    return n + e
}
  , o = function(e) {
    return Math.ceil(e).toString(16).toUpperCase()
}

// e + "-" + t + "-" + n + "-" + r + "-" + o + s((i % 1e5).toString(), 5) + "infoc"
