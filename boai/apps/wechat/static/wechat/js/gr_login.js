var step = 0;
//获取验证码
$("#get_captcha").click(function(){
   // var verify = $("#verify").val();
    var mobile = $("#mobile").val();
    var obj = $(this);
    if(!checkIsMobile(mobile)){
    	addError("mobile");
    	$("#mobile").focus();
    	return false;
    }
    if(step == 0){      //第一次发送短信,后面电话验证
        var type = 1;
    }else {
        var type = 2;
    }
    /*if (/^[0-9a-zA-Z]{4}$/.test(verify) == false) {
    	addError("verify");
        $("#verify").focus();
        return false;
    }*/
    $.post("/Gr/checkVerify/", {mobile:mobile,type:type}, function (data) {
        if (data.status == 1) {
            timeCountDown(obj);
            step++;
        }else if(data.status == 2){
        	addError("mobile");
        }else if(data.status == 3){
        	addError("verify");
        }else{
            alert(data.info);
        }
    }, 'json');
});

//短信验证码基本校验
jQuery.validator.addMethod("isPostiveInterger", function (value) {
	var reg = /^[1-9]{1}[0-9]{3}$/;
	return reg.test(value);
}, "");

//图文验证码基本校验
jQuery.validator.addMethod("isVerify", function (value) {
	var reg = /^[0-9a-zA-Z]{4}$/;
	return reg.test(value);
}, "");

//刷新验证码
$("#verify_img").click(function () {
    $(this).attr("src", "/index/verify/?p=" + Math.random());
});

//表单验证
$("#form-data").validate({
	errorElement: 'em',
	invalidHandler: function(form, validator) {//validate只显示第一个警告
        $.each(validator.invalid,function(key,value){
        	if($("span[for='"+key+"']").length >0 ){
        		$("span[for='"+key+"']").remove();
        	}
        	$("[name='"+key+"']").after("<span for='"+key+"' class='hint'>"+value+"</span>")
        	return false;
        });
	},
	ignore:'',
	rules:{
		mobile:{
			required:true,
			isMobile:true
		},
		verify:{
			required:true,
			isVerify:true
		},
		yanzheng:{
			required:true,
			isPostiveInterger:true,
		},
        password: {
            required:true,
        },
        password2: {
            equalTo: '#password'
        }
	},
	messages:{
		mobile:{
			required:"提示：请填写手机号码",
			isMobile:"提示：请填写正确的手机号码",
		},
		verify:{
			required:"提示：请输入图形验证码",
			isVerify:"提示：请输入正确的图形验证码"
		},
		yanzheng:{
			required:"提示：请输入短信验证码",
			isPostiveInterger:"提示：请输入正确的短信验证码",
		},
        password2: {
                equalTo: "提示：两次密码不一致"
        }
	},
	highlight:function(element){
		$(element).parents(".controls").addClass("error");
	},
    success: function (element) {
    	$(element).parents(".controls").removeClass('error');
    },
    submitHandler:function (form){
    	var postStr = $("#form-data").serialize();
    	$.post("/Gr/doLogin",postStr,function(data){
    		if(data.status == 1){
    			window.location.href="/GrInfo/";
    		}else if(data.status == 2){
    			addError("yanzheng");
    		}else if(data.status == 3){
    			window.location.href="/Gr/notice";
    		}else{
    			alert(data.info)
    		}
    	},'json');
    }
});


//添加错误提示
function addError(id){
	if(!$("#"+id).parent(".controls").hasClass("error")){
		$("#"+id).parent(".controls").addClass("error");
	}
	if(id == "yanzheng"){
		var str = "请输入正确的短信验证码";
	}else if(id == "verify"){
		var str = "请输入正确的图形验证码";
	}else if(id == "mobile"){
		var str = "请输入正确的手机号码";
	}else if(id == "password"){
		var str = "用户名或密码错误";
	}
	$("#"+id).after("<span for='"+id+"' class='hint'>"+str+"</span>");
	/*if($("#"+id).parent(".controls").find(".hint").length == 0){
		$("#"+id).after($("<span for='"+id+"' class='hint'>!</span>"));
	}*/
}

//倒计时
var time = 60;
function timeCountDown(obj){
	if(time == 0){
		obj.attr("disabled",false);
		obj.removeClass("disabled")
		obj.text("试试语音验证码");
		time = 60;
	}else{
		obj.attr("disabled",true);
		obj.addClass("disabled");
		obj.text(time+"S");
		time--;
		setTimeout(function () {
			timeCountDown(obj)
        },
        1000);
	}
}

//提交
$("#doLogin").click(function(){
	$("#form-data").submit();
});



//tab切换
$("#password_login").click(function(){
	$(this).parent().addClass("active");
	$("#captcha_login").parent().removeClass("active");
	$(".password_login").removeClass("hide");
	$(".captcha_login").addClass("hide");
});

$("#captcha_login").click(function(){
	$(this).parent().addClass("active");
	$("#password_login").parent().removeClass("active");
	$(".captcha_login").removeClass("hide");
	$(".password_login").addClass("hide");
});


//密码登录
$("#psLogin").click(function(){
	$("#form-data2").submit();
});

//密码登录表单验证
$("#form-data2").validate({
	errorElement: 'em',
	invalidHandler: function(form, validator) {
        $.each(validator.invalid,function(key,value){
        	if($("span[for='"+key+"']").length >0 ){
        		$("span[for='"+key+"']").remove();
        	}
        	$("[name='"+key+"']").after("<span for='"+key+"' class='hint'>"+value+"</span>")
        	return false;
        });
	},
	ignore:'',
	rules:{
		mobile:{
			required:true,
			isMobile:true
		},
		password:{
			required:true,
		}
	},
	messages:{
		mobile:{
			required:"提示：请填写手机号码",
			isMobile:"提示：请填写正确的手机号码",
		},
		password:{
			required:"提示：请填写密码",
		},
	},
	highlight:function(element){
		$(element).parents(".controls").addClass("error");
	},
    success: function (element) {
    	$(element).parents(".controls").removeClass('error');
    },
    submitHandler:function (form){
    	var postStr = $("#form-data2").serialize();
    	$.post("/Gr/doLogin",postStr,function(data){
    		if(data.status == 1){
    			window.location.href="/GrInfo/";
    		}else if(data.status == 2){
    			addError("password");
    		}else if(data.status == 3){
    			window.location.href="/Gr/notice";
    		}else if(data.status == 4){
    			alert(data.info);
    			$("#mobile").val($("#pwd_mobile").val());
    			$("#captcha_login").click();
    		}else{
    			alert(data.info)
    		}
    	},'json');
    }
});