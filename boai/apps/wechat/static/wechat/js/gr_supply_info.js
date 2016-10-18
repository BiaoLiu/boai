var yg_is_social = $("#yg_is_social").val();
var yg_is_fund = $("#yg_is_fund").val();
changePic();



//城市联动
$("#social_pro").change(function(){
	var obj = $(this);
    var city = obj.val();
    if (city != "") {
        $.post("/index/getChild/", {
            city: city
        }, function (data) {
            //data = "<option value=''>--请选择--</option>\n" + data;
            $("#social_city").html(data);
            showHospital();
            showSocialAcc();
            showFundAcc();
            changePic();
        });
    } else {
        $("#city").html("<option value=''>-请选择城市-</option>");
    }
});


//社保账户状态
$("#social_status").change(function(){
	showHospital();
	showSocialAcc();
})

//公积金账户状态
$("#fund_status").change(function(){
	showHospital();
	showFundAcc();
})


//显示医院
function showHospital(){
	if($("#social_status").val() == 2 && ($("#social_city").val() == 1 || $("#social_city").val() == 17) && yg_is_social == 1){
		$(".hospital-div").removeClass("hide");
	}else{
		$(".hospital-div").addClass("hide");
	}
};


//显示公积金账号(非北京深圳，缴过公积金的需要填写)
function showFundAcc(){
    if ($("#social_city").val() != 1 && $("#social_city").val() != 45
    		&& $("#social_city").val() != 17 && $("#fund_status").val() == 2 && yg_is_fund == 1) {
        $("#fund_acc").removeClass("hide");
    } else {
        $("#fund_acc").addClass("hide");
    }
}


//显示社保电脑号（深圳缴过社保的需要填写）
function showSocialAcc(){
	if($("#social_city").val() == 45 && $("#social_status").val() == 1 && yg_is_social == 1){
		$("#social_acc").removeClass("hide");
	}else{
		$("#social_acc").addClass("hide");
	}
}


//显示白底半身照
function changePic(){
	if(yg_is_social == 1 && ($("#social_city").val() == 1 || $("#social_city").val() == 17) ){
		$("#half_pic").removeClass("hide");
		$(".col3").width("33.333%");
	}else{
		$("#half_pic").addClass("hide");
		$(".col3").width("50%");
	}
}


//表单提交
$("#save-btn").click(function(){
	$("#form-data").submit();
});

//表单验证
$("#form-data").validate({
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
		},
		social_status:{
			required:true
		},
		fund_status:{
			required:true
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
		},
		social_status:{
			required:"提示：请选择社保状态"
		},
		fund_status:{
			required:"提示：请选择公积金状态"
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
    	$.post("/GrInfo/saveSupplyInfo",postStr,function(data){
    		if(data.status == 1){
    			alert("修改完成");
    			window.location.href="/GrInfo/otherInfo";
    		}else{
    			alert(data.info);
    		}
    	},'json');
    }
});

//微信上传
wx.ready(function () {
	// 图片接口->拍照、本地选图
    var images = {
        localId: [],
        serverId: []
    };
    var i = 0, length = images.localId.length;
    images.serverId = [];

    $('.upload-pic').click(function(){
    	var type = $(this).attr("type");
        $("#upload").attr("tval", type);
        choose_img();
    });


    //选图并上传img_type=1头像2非头像
    function choose_img() {
        wx.chooseImage({
            success: function (res) {
                images.localId = res.localIds;
                upload();
            }
        });
    }

    //上传图片到微信
    function upload() {
        wx.uploadImage({
            localId: images.localId[i],
            isShowProgressTips: 1,// 默认为1，显示进度提示
            success: function (res) {
                images.serverId = res.serverId;
                ajaxFile();//将需要的数据post
            },
            fail: function (res) {
                alert(JSON.stringify(res));
            }
        });
    }


    //从微信取回图片
    function ajaxFile() {
        var obj = $("#upload");
        var type = obj.attr("tval");

        $.post("/GrInfo/infoPicture", {
            serverId: images.serverId,
            type: type
        }, function (data) {
            if (data.status == 1) {
                $("." + type).replaceWith("<img src='" + data.info.show_path + "' class='d-ib "+type+"'/>");
            } else {
                alert(data.info);
            }
        }, 'json');
        return false;
    }
});


