/**********************************DOM自身事件,属性相关 ***************************/
//浏览器判断
//调用方法 : alert(window.sys.ie) → 弹出ie为ie几
(function () {
    window.sys = {}; //外部可访问
    var ua = navigator.userAgent.toLowerCase();
    var s; // 浏览器信息数组
    //三元选择
    (s = ua.match(/msie ([\d.]+)/)) ? sys.ie = s[1] :
        (s = ua.match(/firefox\/([\d.]+)/)) ? sys.firefox = s[1] :
            (s = ua.match(/chrome\/([\d.]+)/)) ? sys.chrome = s[1] :
                (s = ua.match(/opera\/.*version\/([\d.]+)/)) ? sys.opera = s[1] :
                    (s = ua.match(/version\/([\d.]+).*safari/)) ? sys.safari = s[1] : 0;

    if (/webkit/.test(ua)) sys.webkit = ua.match(/webkit\/([\d]+)/)[1]; //webkit内核

    //平台、设备和操作系统
    sys.win = false;
    sys.mac = false;
    sys.xll = false;
    sys.ipad = false;

    //检测平台
    sys.pt = navigator.platform;
    sys.win = sys.pt.indexOf("Win") == 0;
    sys.mac = sys.pt.indexOf("Mac") == 0;
    sys.x11 = (sys.pt == "X11") || (sys.pt.indexOf("Linux") == 0);
    sys.ipad = (navigator.userAgent.match(/iPad/i) != null) ? true : false;
    //跳转语句，如果是手机访问就自动跳转到wap.baidu.com页面
    if (sys.win || sys.mac || sys.xll || sys.ipad) {
        sys.mobie = false;  //非手机
    } else {
        sys.mobie = true;  //手机
    }
})()


//删除左右空格
function trim(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

//each函数
function each(arr, fn, isJson) {
    if (!fn || (arr.length == 0)) {
        return;
    }
    if (arr.length) { // 如果有长度 , 那么这是一个数组,用for循环
        for (var i = 0, len = arr.length; i < len; i++) {
            if (arr[i].length && typeof(arr[i]) != 'string') { //若为多维数组 ;
                each(arr[i], fn);
            } else {
                fn.call(arr[i], i);
            }
        }
    } else {
        if (isJson) {
            this.i || (this.i = 0);
            for (this.i in arr) {
                fn.call(arr[this.i], i)
            }
        } else { //如果不是数组 ,又不是json , 也误用了each方法,  那就先把这单个元素转换为长度为1的数组.
            var _arr = [];
            _arr.push(arr);
            arr = _arr;
            each(arr, fn);
        }
    }
}

//在最前面appendChild
function prependChild(parent, newChild) {
    if (parent.firstChild) {
        parent.insertBefore(newChild, parent.firstChild);
    } else {
        parent.appendChild(newChild);
    }

    return parent;
}

//事件绑定 (好奇怪 ,IE8以下不兼容)
function addEvent(obj, type, fn) {
    if (obj.addEventListener) { //非IE
        obj.addEventListener(type, fn, false);
    } else {
        obj.attachEvent("on" + type, function () { //兼容IE
            fn.call(obj);
        })
    }
}
//事件绑定
function bindEvent(obj, event, fnCallback) {
    if (obj.addEventListener) { //非IE
        obj.addEventListener(event, fnCallback, false);
    } else {
        obj.attachEvent("on" + event, function () { //兼容IE
            fnCallback.call(obj);
        })
    }
};
//解除事件绑定
function removeBind(obj, type, fn) {
    if (obj.removeEventListener) {
        obj.removeEventListener(type, fn, false);
    } else {
        obj.detachEvent('on' + type, function () {
            fn.call(obj);
        });
    }
};


/**************************************简化版面向对象*************************************/
// 选择与执行函数 : 
//前台调用
function So(args) {
    return new Base(args);
}

//基类
function Base(args) {
    this.elements = [];
    var _this = this;
    if (typeof args == "string") {
        var elements = trim(args).split(/\s+/);
        if (elements.length > 1) {
            var parentNode = [document]; // 默认document为父节点
            var childNode = [] //储存获取的节点
            for (var i = 0; i < elements.length; i++) {
                switch (elements[i].charAt(0)) {
                    case "#":
                        parentNode = [];
                        childNode = [];
                        childNode.push(_this.getId(elements[i].substring(1)));
                        parentNode = childNode;
                        break;
                    case ".":
                        childNode = [];
                        for (var j = 0; j < parentNode.length; j++) {
                            var temps = this.getClass(elements[i].substring(1), null, parentNode[j]);
                            for (var k = 0; k < temps.length; k++) {
                                childNode.push(temps[k]);
                            }
                        }
                        parentNode = childNode;
                        break;
                    default:
                        childNode = [];

                        for (var j = 0; j < parentNode.length; j++) {
                            var temps = this.getTag(elements[i], parentNode[j]);
                            for (var k = 0; k < temps.length; k++) {
                                childNode.push(temps[k]);
                            }
                        }
                        parentNode = childNode;
                        break;
                }
            }

            this.elements = childNode;
        } else {
            //find模拟
            switch (args.charAt(0)) {
                case "#":
                    this.elements.push(this.getId(args.substring(1)));
                    break;
                case ".":
                    each(this.getClass(args.substring(1)), function () {
                        _this.elements.push(this);
                    })
                    break;
                default:
                    each(this.getTag(args), function () {
                        _this.elements.push(this);
                    })
                    break;
            }
        }
    } else if (typeof args == "object") {
        if (args != undefine) {
            this.elements[0] = args;
        }
    } else if (typeof args == "function") {
        this.ready(args);
    }
}

// 原型方法
Base.prototype = {
    //就绪
    ready: function (args) {
        addDomLoaded(args);
    },
    //选择函数的find函数
    find: function (str) {
        var childElements = [];
        var _this = this;

        each(this.elements, function () {
            switch (str.charAt(0)) {
                case "#":
                    childElements.push(_this.getId(str.substring(1)));
                    break;
                case ".":
                    each(_this.getClass(str.substring(1), null, this), function () {
                        childElements.push(this);
                    })
                    break;
                default:
                    each(_this.getTag(str, this), function () {
                        childElements.push(this);
                    })
                    break;
            }
        })
        this.elements = childElements;
        return this;
    },
    //获取元素
    getId: function (id) {
        return document.getElementById(id);
    },
    getTag: function (tag, pNode) {
        pNode = (pNode) ? pNode : document; //如果未传入上级 ,则默认为document ;
        var tags = pNode.getElementsByTagName(tag);
        return tags;
    },
    getClass: function (sClass, sTagName, pNode) {
        pNode = (pNode) ? pNode : document;
        var allChildNode = [];
        if (pNode.getElementsByClassName) {
            allChildNode = pNode.getElementsByClassName(sClass);
        } else {
            sTagName = (sTagName) ? sTagName : "*"; // 若没有传入标签
            var _all = document.getElementsByTagName(sTagName);
            for (var i = 0, len = _all.length; i < len; i++) {
                var allClass = _all[i].className.split(/\s+/); //若单个元素有多重标签
                for (var j = 0; j < allClass.length; j++) {
                    if (allClass[j] == sClass) {
                        allChildNode.push(_all[i]);
                    }
                }
            }
        }
        return allChildNode;
    },
    css: function (attr, value) {

        if (typeof value === "number" && attr != "opacity") {
            value = value + "px";
        }
        for (var i = 0, len = this.elements.length; i < len; i++) {
            if (arguments.length == 1) {
                if (this.elements[i].currentStyle) {
                    return this.elements[i].currentStyle[attr];
                } else {
                    return getComputedStyle(this.elements[i], false)[attr];
                }
            } else {
                this.elements[i].style[attr] = value;
            }
        }
        return this;
    },
    center: function (json, fn, parentNode) {
        each(this.elements, function () {
            var selfW = (json) ? json.width : parseInt(getStyle(this, "width"));
            var selfH = (json) ? json.height : parseInt(getStyle(this, "height"));
            var wW = (parentNode) ? parentNode.css("width") : getClient().w;
            var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            var wH = (parentNode) ? parentNode.css("height") : getClient().h;
            var l = Math.round((wW - selfW) / 2);
            var t = Math.round((wH - selfH) / 2 + scrollTop);
            this.l = l;
            this.t = t
            tStartMove(this, {
                width: selfW,
                height: selfH,
                left: l,
                top: t
            }, function () {
                if (fn) fn();
            }, "elasticOut");
        })
        return this;
    },
    //添加link或style的css规则
    addRule: function (num, selectorText, cssText, index) {
        var sheet = document.styleSheets[num];
        index = (index) ? index : 0;
        addRule(sheet, selectorText, cssText, index);
        return this;
    },
    //移除规则表的项
    removeRule: function (num, index) {
        var sheet = document.styleSheets[num];
        index = (index) ? index : 0;
        removeRule(sheet, index);
        return this;
    },
    html: function (str) {
        for (var i = 0; i < this.elements.length; i++) {
            if (!str) {
                return this.elements[i].innerHTML;
            } else {
                this.elements[i].innerHTML = str;
            }
        }
        return this;
    },
    //得到输入框或其他的内在内容
    value: function (str) {
        for (var i = 0; i < this.elements.length; i++) {
            if (!str) {
                return this.elements[i].value;
            } else {
                this.elements[i].value = str;
            }
        }
        return this;
    },
    //设置元素属性
    setAttr: function (attr, value) {
        each(this.elements, function () {
            this.setAttribute(attr, value);
        })
    },
    hover: function (hover, out) {
        each(this.elements, function (index) {
            this.onmouseover = function () {
                hover.call(this, index);
            }
            this.onmouseout = function () {
                out.call(this, index);
            }
        })
    },
    eq: function (index) {
        if (index == 1) {
            return this.elements[0];
        }
        else if (index == -1) {
            return this.elements[this.elements.length - 1];
        }
        else {
            return this.elements;
        }
    },
    show: function () {
        each(this.elements, function () {
            this.style.display = "block";
        })
    },
    hidden: function () {
        each(this.elements, function () {
            this.style.display = "none";
        })
    },
    click: function (fnCallback) {
        each(this.elements, function () {
            this.onclick = fnCallback;
            this.click = fnCallback;
        })
    },
    //事件(onkeydown等)
    bind: function (event, fn) {
        each(this.elements, function () {
            addEvent(this, event, fn);
        })
    },
    // 拖拽
    drag: function (dragAble, dir, target, rangejson, fnMove) {
        each(this.elements, function () {
            drag(this, dragAble, dir, target, rangejson, fnMove);
        })
    },
    //插件入口
    extend: function (name, fn) {
        Base.prototype[name] = fn;
    },
    //运动
    startMove: function (json, fn) {
        each(this.elements, function () {
            if (fn) {
                startMove(this, json, fn);
            } else {
                startMove(this, json);
            }
        })
    },
    GetQueryString: function (param) {  // 获取地址栏的s和t的值
        var reg = new RegExp("(^|&)" + param + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null)return unescape(r[2]);
        return null;
    },
    //Tween运动
    tStartMove: function (json, fn) {
        each(this.elements, function () {
            if (fn) {
                tStartMove(this, json, fn);
            } else if (!fn) {
                tStartMove(this, json);
            }
        })
    },
    writeCookie: function (obj, expiresT) {
        for (var attr in obj) {
            // if(key&&value){
            var _writeCookie = attr + '=' + obj[attr];
            if (expiresT) {
                var date = new Date();
                date.setTime(date.getTime() + expiresT * 60 * 1000);
                _writeCookie += (';expires=' + date.toGMTString());
            }
            document.cookie = _writeCookie;
            // }
        }
    },
    getCookie: function (cookieName) {
        if (!cookieName) {
            return null;
        }
        if (document.cookie.indexOf(cookieName) !== -1) {
            var cs = document.cookie.split(';'),
                i = 0,
                len = cs.length;
            for (; i < len; i++) {
                if (cs[i].split('=')[0].trim() === cookieName) {
                    return cs[i].split('=')[1];
                }
            }
        }
        return null;
    }
}

So.each = function (arr, fn) {
    if (!arr.length || fn) {
        return;
    }
    for (var i = 0, len = arr.length; i < len; i++) {
        fn.call(this, i);
    }
}

// 省市区三级联动
// if 传入元素 , 找到元素写入 ;
// if 没有传入元素 ,则返回数据让外部函数调用
var LinkAge = function (args) {
    return new LinkAge.prototype.init(args);
}

LinkAge.prototype = {
    constructor: LinkAge,
    init: function (args) {
        if (args) { //如果有参数 , 则给参数对象绑定事件 ,以及其他处理
            for (var attr in args) {
                this[attr] = args[attr];
            }
            this.getALlData();
            this.dealPro();
            this.bind();
            if (this.provinceEl && this.provinceEl.getAttribute('data-default')) { //如果有省默认值
                var $this = this;
                this.proNow = this.provinceEl.getAttribute('data-default');
                this.provinceEl.value = this.proNow;

                if (this.cityEl && this.cityEl.getAttribute('data-default')) { //如果有省默认值
                    this.cityNow = this.cityEl.getAttribute('data-default');
                    this.getCityByPro();
                    this.cityEl.value = this.cityNow;

                    if (this.districtEl && (this.districtEl.getAttribute('data-default') || this.districtEl.getAttribute('data-default') === "")) { //如果有省默认值
                        this.disNow = this.districtEl.getAttribute('data-default') || "请选择";
                        //如果是输入框,直接输出
                        if (this.districtEl.tagName == 'INPUT') {
                            this.districtEl.value = this.districtEl.getAttribute('data-default');
                        }
                        else if (this.districtEl.tagName == 'SELECT') { //如果是选择下拉
                            this.getDisByCity();
                            this.districtEl.value = this.disNow;
                        }
                    }
                }
            }
        } else { //否则直接返回一个实例 ,方便调用方法
            this.getALlData();
            this.dealPro();
            return this;
        }
    },
    getALlData: function () {
        var _this = this;
        if (!this.data && !window.mapCity) {
            $.ajax({
                type: 'POST',
                url: "http://www.pvplus.com.cn/ajax/ajax_getmap.aspx?type=all",
                cache: false,
                async: false,
                dataType: "json",
                success: function (res) {
                    _this.data = res;
                    _formatData(res);
                    return _this.data;
                }
            });
        } else { //暂存城市列表 , 一个多个地方选择避免每次都get
            this.data = window.mapCity || this.data;
        }

        function _formatData(data) {
            var _formatedData = [];

            for (var i = 0, iLen = data.length; i < iLen; i++) {
                _formatedData[i] = {};
                _formatedData[i].pro = data[i].pro; //省格式

                _formatedData[i].city = []; //数组中弹出市格式
                _formatedData[i].dis = []; //相应城市下的区为一个数组元素

                for (var j = 0, jLen = data[i].city.length; j < jLen; j++) {
                    var _oCityAndDis = data[i].city[j].split('|');
                    _formatedData[i].city.push(_oCityAndDis.shift()); //数组中弹出市格式
                    _formatedData[i].dis.push(_oCityAndDis); //相应城市下的区为一个数组元素
                }
            }
            if (_this.provinceEl.getAttribute('data-hasAll')) {  //如果有全国往数组前
                _formatedData.unshift({
                    city: [],
                    dis: [],
                    pro: "全国"
                })
            }
            _this.data = _formatedData;
            window.mapCity = _formatedData; //window对象暂存城市地图
        }

        return this;
    },
    dealPro: function () {
        var _proArr = [];
        each(this.data, function () {
            _proArr.push(this['pro']);
        })
        this.addOption({
            el: this.provinceEl,
            data: _proArr
        });
        this.proData = _proArr;
        return this;
    },
    getCityByPro: function () { //根据省来获得市,顺便可以获得省在data的下标
        this.proNow = this.proNow || arguments[0];
        var _this = this;
        var _cityArr = [];

        for (var i = 0, proLen = this.data.length; i < proLen; i++) {
            var _loopNow = this.data[i];
            if (_loopNow['pro'] == _this.proNow) {
                _this.proIndex = i; // 当前省在data的下标
                _cityArr = _loopNow['city'];
                _this.activeCityData = _cityArr;
                break;
            }
        }

        this.addOption({
            el: this.cityEl,
            data: _cityArr
        });

        if (this.districtEl && this.districtEl.tagName == 'INPUT') {
            this.districtEl.value = '';
        }
        return this;
    },
    getDisByCity: function () {
        var _this = this;
        this.cityNow = this.cityNow || arguments[0];
        var _disArr = [];

        var _cityArr = this.data[this.proIndex].city;
        for (var i = 0, cityLen = _cityArr.length; i < cityLen; i++) {
            var _loopNow = _cityArr[i];
            if (_loopNow == _this.cityNow) {
                _this.cityIndex = i; //获取当前城市的数组下标
                break;
            }
        }

        _disArr = this.data[this.proIndex].dis[this.cityIndex];
        if (this.districtEl && this.districtEl.tagName == 'INPUT') {
            this.districtEl.value = '';
        }
        else if (this.districtEl && this.districtEl.tagName == 'SELECT') {
            this.addOption({
                el: this.districtEl,
                data: _disArr
            });
        }
        this.activeDisData = _disArr;
        return this;
    },
    succGetPro: function (callback) { //获得省回调
        if (callback) {
            this.succGetPro = callback(this.proData);
        }
        return this;
    },
    succGetCity: function (callback) { //获得市回调
        if (callback) {
            this.succGetCity = callback(this.activeCityData);
        }
        return this;
    },
    succGetDis: function (callback) { //获得区回调
        if (callback) {
            this.succGetDis = callback(this.activeDisData);
        }
        return this;
    },
    addOption: function (obj) {
        if (!obj.el) {
            return;
        }
        if (parseInt(sys.ie) < 10) { //如果为IE10以下
            obj.el.innerHTML = '';
            var _option = document.createElement('option');
            _option.value = '请选择';
            _option.innerHTML = '请选择';
            obj.el.appendChild(_option);

            each(obj.data, function () {
                var _option = document.createElement('option');
                _option.value = this;
                _option.innerHTML = this;
                obj.el.appendChild(_option);
            })
        } else {
            var _str = '<option value="请选择">请选择</option>';
            each(obj.data, function () {
                _str += '<option value="' + this + '">' + this + '</option>';
            })
            obj.el.innerHTML = _str;
        }
    },
    resetDis: function () {
        this.districtEl.innerHTML = '';
        var _option = document.createElement('option');
        _option.value = '请选择';
        _option.innerHTML = '请选择';
        this.districtEl.appendChild(_option);
    },
    bind: function () {
        var _this = this;
        //绑定省元素的数据切换 :刷新市 刷新区为默认
        bindEvent(this.provinceEl, 'change', function (index) {
            _this.proNow = this.value;
            _this.getCityByPro();
            if (_this.districtEl) { //如果有区级
                _this.resetDis();
            }
        })

        //绑定市元素的数据切换
        bindEvent(this.cityEl, 'change', function (index) {
            _this.cityNow = this.value;
            if (_this.districtEl) {
                _this.getDisByCity();
            }
        })
    }
}

LinkAge.prototype.init.prototype = LinkAge.prototype;


    
