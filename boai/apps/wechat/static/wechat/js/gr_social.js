//是否缴社保，公积金
$(".choose_box").click(function(){
	var str = $(this).attr("id");

	if($(this).is(":checked")){
		if(str == "salary"){
			$("#salary_div").removeClass("hide");
		}else{
			$("#yg_is_"+str).val(1);
		}
	}else{
		if(str == "salary"){
			$("#salary_div").addClass("hide");
			$("#yg_salary").val(0);
		}else{
			$("#yg_is_"+str).val(0);
		}


	}
	showRule();
	$(this).siblings("span").toggleClass("active");
	$("."+str+"_div").toggleClass("hide");
	var is_social	=	$("#yg_is_social").val();
	var is_fund		=	$("#yg_is_fund").val();
	if(is_social==0&&is_fund==0) {
		$(".time").toggleClass("hide");
	}else
	{
		$(".time").show();
	}
	$("#form-data").submit();
});

//显示社保公积金规则
function showRule(){
	if($("#yg_is_social").val() == 1){
		if($("#hide_social_rule").length > 1){
			$(".social_rule_div").removeClass("hide");
		}
	}else{
		$(".social_rule_div").addClass("hide");
	}
	if($("#yg_is_fund").val() == 1){
		if($("#hide_fund_rule").length > 1){
			$(".fund_rule_div").removeClass("hide");
		}
	}else{
		$(".fund_rule_div").addClass("hide");
	}
}

//税前税后
$("input[name='salary_type']").click(function(){
	$(this).parents(".control-group").children("label").toggleClass("off");
	$("#form-data").submit();
});



//验证社保基数
jQuery.validator.addMethod('isSocialBasic', function (value) {
	var str = $("#social_range").val();
	var range = str.split("-");
	var min = parseFloat(range[0]);
	var max = parseFloat(range[1]);
	return isSalary(value) && value >= min && value <= max;
}, '社保基数填写超出范围');



//验证公积金基数
jQuery.validator.addMethod('isFundBasic', function (value) {
	var str = $("#fund_range").val();
	var range = str.split("-");
	var min = parseFloat(range[0]);
	var max = parseFloat(range[1]);
	return isSalary(value) && value >= min && value <= max;
}, '公积金基数填写超出范围');


//输入框提交
$("input[type='number']").blur(function(){
	$("#form-data").submit();
});
$("select").change(function(){
	$("#form-data").submit();
});


//获取基数范围提示
function getRangeAlert($type){
	var str = $("#"+$type+"_range").val();
	var range = str.split("-");
	var min = parseFloat(range[0]);
	var max = parseFloat(range[1]);
	return "提示：基数范围必须在"+min+"至"+max+"之间";
}



//表单验证
$("#form-data").validate({
	errorElement: 'em',
	invalidHandler: function(form, validator) {//validate只显示第一个警告
        $.each(validator.invalid,function(key,value){
        	if($("span[for='"+key+"']").length >0 ){
        		return false;
        	}
        	$("[name='"+key+"']").after("<span for='"+key+"' class='hint'>"+value+"</span>")
        	return false;
        });
	},
	rules:{
		yg_is_social:{
			required:true
		},
		social_basic:{
			required:true,
			isSocialBasic:true
		},
		time_start:{
			required:true,
		},
		yg_is_fund:{
			required:true,
		},
		fund_basic:{
			required:true,
			isFundBasic:true
		},
		time_end:{
			required:true
		},
		salary_type:{
			required:true
		}

	},
	messages:{
		yg_is_social:{
			required:"提示：请选择是否缴纳社保"
		},
		social_basic:{
			required:"提示：请填写社保基数",
			isSocialBasic:getRangeAlert("social"),
		},
		time_start:{
			required:"提示：请选择起缴月份"
		},
		yg_is_fund:{
			required:"提示：请选择是否缴纳公积金",
		},
		fund_basic:{
			required:"提示：请填写公积金基数",
			isFundBasic:getRangeAlert("fund")
		},
		time_end:{
			required:"提示：请选择结束月份"
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
		$.post("http://weixin.mayihr.com/GrSocial/calculateSocial/",postStr,function(data){
		    alert(data.status);
			if(data.status == 1){
				$("#bill_detail").html(data.info.html_div);
				$("#all_money").html(data.info.all_money+"元");
			}else{
				alert(data.info);
				return false;
			}
		},'json');
    }
});


//确认账单
$("#pay-btn").click(function(){
	if(parseFloat($("#all_money").text()) <= 0){
		alert("请完善信息并计算后再确认账单");
		return false;
	}
	$.post("/GrPay/createBill",{action:"create_bill"},function(data){
		if(data.status == 1){
			window.location.href="/GrPay/index";
		}else if(data.status == 2){
			alert(data.info);
			window.location.href="/GrPay/unpayedOrder/";
		}else{
			alert(data.info);
		}
	},'json');
})

if(is_show == 1){
    modal('save','show');
}