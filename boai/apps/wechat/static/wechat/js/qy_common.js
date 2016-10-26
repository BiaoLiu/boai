//检查正数
function checkPositive(num){
    var reg = new RegExp("^-?[0-9]*.?[0-9]*$");
    if ( reg.test(num) ) {
        var absVal = Math.abs(num);
        if(num != absVal){  //是负数
            return false;
        }
    }else {
        return false;
    }
    return true;
}
$('body').on('click','.modal .cancel',function() {
    $(this).parents('.modal').hide();
    $('.back-drop').remove();
});
$('body').on('click','.back-drop',function() {
    $('.modal').hide();
    $('.back-drop').remove();
});


//新弹窗modal

function modal(obj,state,callback){

    if(state == 'show') {
        $('.modal.'+ obj).show();
        if($('.back-drop').length == 0){
            $('<div class="back-drop pf"></div>').appendTo('body');
        }
    } else if(state == "hide") {
        $('.modal.'+ obj).hide();
        $('.back-drop').remove();
        if(typeof callback === 'function') {
           callback();
       }

        $('.modal.'+ obj).off('click', '.btn.confirm');
        $('.modal.'+ obj).off('click', '.btn.cancel');
   }
   //绑定按钮事件
   $('.modal.'+ obj).on('click', '.btn.confirm', function() {
        if(callback) {
            modal(obj, 'hide', callback.confirm);
        }else {
            modal(obj, 'hide');
        }
    });
   $('.modal.'+ obj).on('click', '.btn.cancel', function() {
        if(callback) {
               modal(obj, 'hide', callback.cancel);
           }else {
               modal(obj, 'hide');
           }
    });
}
var POPUP = {
    alert: function(title,content,callback) {
        $('.alert .p_title').text(title);
        $('.alert .p_msg').text(content);
        modal('alert', 'show',callback);
    },
    //
    confirm: function(msg,callback) {
        $('.confirm .p_title').text(msg.title);
        $('.confirm .p_msg').text(msg.content);
        modal('confirm', 'show',callback);
    },
    pop: function(state,msg,callback) {//state:绿色.success,红色.warning
        $('.modal').addClass(state);
        $('.pop .p_title').text(msg.title);
        $('.pop .p_msg').text(msg.content);
        modal('pop', 'show');
        var timer = null;
        timer = setTimeout(function() {
            if(callback){
                modal('pop', 'hide', callback.confirm);
            }
            else {
                modal('pop', 'hide');
            }
            clearTimeout(timer);
        }, 1000);
    }

};