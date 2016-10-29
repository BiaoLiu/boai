// 仿IOS7 DatePicker
//
/*
      QQ:158954945   个人学习
      主做IOS，由于工作需要刚开始学习web,不喜勿喷，欢迎指正

            初始化参数
            初始化UI
            初始化iScroll
            滚动iScroll修改UI
*/
/*
  scroll : iScroll
  index  : selectIndex
  type   : yyyy
  start  : 1970
  end    : 2020
  refresh();
*/


(function ($) {
  $.fn.mydate = function (options,Ycallback,Ncallback) {
    var that = $(this);
    var itemsArray = new Array();   //存放有几列数据的数组
    var myDate = new Date();
    var year=myDate.getFullYear();
    var month=myDate.getMonth()+1;
    $.fn.mydate.defaultOptions = {
      format:"yyyy,MM,dd",
      beginyear:year,
      endyear  :year+1,
      startyear:year,
      currdate :true
    }
    var opts = $.extend( true, {}, $.fn.mydate.defaultOptions, options);

    initParam();
    initUI();
    initCss();
    initScroll();
    initAction();

    $("#mDatePicker").css({"bottom":"0"});

    function initParam () {
      var formatItems = opts.format.split(',');
      for (var i in formatItems) {
        var item =  itemObject(formatItems[i]);
        if (item != null ) itemsArray.push(item);
      }
    }

    function initUI(){
      $("#mDateMask").show();
      $("#mDateMask").html(pickerContent());
      var pickerHtml = $("#mDatePicker").html();
      for (var i in itemsArray) {
        var item =  itemsArray[i];
        item.bulidUI();
        pickerHtml += item.ui;
      }
      $("#mDatePicker").html(pickerHtml);
    }

    function initCss () {
      $("#mDatePicker div").css({"width":100/(itemsArray.length)+"%"});
    }

    function initScroll () {
      for (var i in itemsArray) {
        var item = itemsArray[i];
        item.refresh();
      }
      if (opts.currdate) {
        setScrollDate(new Date());
      }
    }

    function setScrollDate (datetime) {
      var year=parseInt((datetime.getFullYear()));
      var month=parseInt(datetime.getMonth())+1;
      var day=parseInt(datetime.getDate());
      var hour=parseInt(datetime.getHours());
      var minutes=parseInt(datetime.getMinutes());
      var second =parseInt(datetime.getSeconds());

      for (var i in itemsArray) {
        var item = itemsArray[i];
        if (item.type == "yyyy") {
          item.index = year - item.min + 1;
        }else if (item.type == "MM") {
          item.index = month - item.min + 1;
        }else if (item.type == "dd") {
          item.index = day - item.min + 1;
        }else if (item.type == "HH") {
          item.index = hour - item.min + 1;
        }else if (item.type == "mm") {
          item.index = minutes - item.min + 1;
        }else if (item.type == "ss") {
          item.index = second - item.min + 1;
        }
        item.refresh();
      }
    }

    function initAction(){
      $("#mDatePicker .finish-btn").click(function(){
        $("#mDatePicker").css({"bottom":"-275px"});
        setTimeout('$("#mDateMask").hide()',500);
        var resultStr = "";
        for (var i in itemsArray) {
          var item = itemsArray[i];
          resultStr += item.toText();
        }
        if (Ycallback == undefined) {
          if (that.is('input')) {
            that.val(resultStr);
          }else {
            that.html(resultStr);
          }
        }else {
          Ycallback(resultStr);
        }
      });
    }

    function newPicker(idStr) {
      return new iScroll(idStr,{snap:"li",vScrollbar:false,
          onScrollEnd:function () {
            var selectIndex = Math.round(this.y/(-60)) + 1;
            for (var i in itemsArray) {
              var item = itemsArray[i];
              if (item.pickerName == idStr ) {
                item.index = selectIndex;
                if (item.type == "yyyy" || item.type == "MM") {
                  adjustDays();
                }
              }
            }
          }});
    }

    function adjustDays () {
      var year = parseInt((new Date().getFullYear()));
      var month = parseInt((new Date().getMonth()));
      var yearItem,monthItem,dayItem;
      for (var i in itemsArray) {
        var item = itemsArray[i];
        if (item.type == "yyyy") {
          yearItem = item;
          year     = item.min + item.index -1 ;
        }else if (item.type == "MM") {
          monthItem = item;
          month     = item.min + item.index -1 ;
        }else if (item.type == "dd") {
          dayItem = item;
        }
      }
      if (dayItem == null)return;
      var days = new Date(year,month,0).getDate();
      if (days != dayItem.max) {
        dayItem.reSetMax(days);
      }
    }

    function itemObject (type) {
      var obj = new Object();
      obj.type = type;
      obj.index = 1;
      switch (type) {
        case "yyyy":
          obj.pickerName = "yearPicker";
          obj.min = opts.beginyear;
          obj.max = opts.endyear;
          obj.unit = '年';
          break;
        case "MM":
          obj.pickerName = "monthPicker";
          obj.min = month;
          obj.max = 12;
          obj.unit = '月';
          break;
        case "dd":
          obj.min = 1;
          obj.max = 31;
          obj.pickerName = "dayPicker";
          obj.unit = '日';
          break;
        case "am":
          obj.ui = initAmUI();
          obj.min = 1;
          obj.max = 2;
          obj.pickerName = "amPicker";
          break;
        case "HH":
          obj.min = 1;
          obj.max = 24;
          obj.pickerName = "hhPicker";
          obj.unit = '时';
          break;
        case "mm":
          obj.min = 0;
          obj.max = 59;
          obj.pickerName = "mmPicker";
          obj.unit = '分';
          break;
        case "ss":
          obj.min = 0;
          obj.max = 59;
          obj.pickerName = "ssPicker";
          obj.unit = '秒';
          break;
        default :
           return null;
          break;
      }
      obj.bulidUI = function() {
        if (obj.ui == null) {
          obj.ui = initItemsUI(obj.pickerName,obj.unit,obj.min,obj.max);
        }
      }

      obj.refresh = function() {
        if (obj.picker == null) {
          obj.picker = newPicker(obj.pickerName);
        }
        obj.picker.refresh();
        obj.picker.scrollTo(0,60*(obj.index - 1),400,true);
      }

      obj.toText = function () {
        if (obj.type == "am") {
          if (obj.index == 1) {return "上午";
          }else if(obj.index == 2){return "下午";}
        }else {
          return (obj.min + obj.index-1) + obj.unit;
        }
      }

      obj.reSetMax = function (num) {
        obj.max = num;
        $("#"+obj.pickerName).find("ul li").each(function(i){
          if (i < num+1) {$(this).show();}else {$(this).hide();}
        });
        $("#"+obj.pickerName).find("ul li:last").show();
        obj.picker.refresh();
      }
      return obj;
    }

    function pickerContent() {
      return '<div id = "mDatePicker"><section class="picker-tool"><span class = "picker-flg"></span><p class= "finish-btn">完成</p></section></div>'
    }

    function initItemsUI (idStr,unit,begin,end) {
      var str=  "<div id= " + idStr + "><ul><li>&nbsp;</li>";
      for(var i=begin; i<=end;i++){str+='<li>'+i+unit+'</li>'}
      return str+"<li>&nbsp;</li></ul></div>";
    }

    function initAmUI() {
      return "<div id='amPicker'><ul><li>&nbsp;</li><li>上午</li><li>下午</li><li >&nbsp;</li></ul></div>"
    }
  }
})(jQuery);
