$("#social_pro").change(function(){
	var obj = $(this);
    var city = obj.val();
    if (city != "") {
        $.post("/index/getChild/", {
            city: city
        }, function (data) {
            //data = "<option value=''>--请选择--</option>\n" + data;
            $("#social_city").html(data);
        });
    } else {
        $("#city").html("<option value=''>-请选择城市-</option>");
    }
});

//表单提交
$("#save-btn").click(function(){
	$("#basic-form").submit();
});

//表单验证
$("#basic-form").validate({
	errorElement: 'em',
	invalidHandler: function(form, validator) {//validate只显示第一个警告
        $.each(validator.invalid,function(key,value){
        	if($("span[for='"+key+"']").length >0 ){
        		return false;
        	}
        	$("[name='"+key+"']").after("<span for='"+key+"' class='hint'>"+value+"</span>")
        });
	},
	rules:{
		yg_name:{
			required:true,
			checkName:true,
		},
		yg_phone:{
			required:true,
			isMobile:true
		},
		yg_email:{
			required:true,
			isEmail:true
		},
		yg_identity:{
			required:true,
			isCard:true
		}
	},
	messages:{
		yg_name:{
			required:"提示：请填写您的姓名",
			checkName:"提示：请填写正确的姓名（不包含特殊字符）",
		},
		yg_phone:{
			required:"提示：请填写您的手机号码",
			isMobile:"提示：请填写正确的手机号码",
		},
		yg_email:{
			required:"提示：请填写您的邮箱",
			isEmail:"提示：请填写正确的邮箱"
		},
		yg_identity:{
			required:"提示：请填写您的身份证",
			isCard:"提示：请填写正确的身份证号码"
		}
	},
	highlight:function(element){
		$(element).parents(".controls").addClass("error");
	},
    success: function (element) {
    	$(element).parents(".controls").removeClass('error');
    },
    submitHandler:function (form){
    	var postStr = $("#basic-form").serialize();
    	$.post("/GrInfo/saveBasic",postStr,function(data){
    		if(data.status == 1){
    			window.location.href="/GrSocial/";
    		}else{
    			alert(data.info);
    		}
    	},'json');
    }
});