//js把日期字符串转换成时间戳
function get_unix_time(dateStr)
{
var newstr = dateStr.replace(/-/g,'/');
    var date =  new Date(newstr);
    var time_str = date.getTime().toString();
    return time_str.substr(0, 10);
}
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

//验证起缴日期大于当前日期
jQuery.validator.addMethod('isTimeBig', function (value) {
	time_s=$('.time_start').val();
	console.log(get_unix_time(time_s));
	time_s=time_s.split('.');
	year_s=parseInt(time_s[0]);
	month_s=parseInt(time_s[1]);

	time_e=$('.time_end').val();
	time_e=time_e.split('.');
	year_e=parseInt(time_e[0]);
	month_e=parseInt(time_e[1]);

	var myDate = new Date();
	var year=myDate.getFullYear();
	var month=myDate.getMonth()+1;
	if(year_s>year||(year_s==year&&month_s>=month))
	{
		return true;
	}else
	{
		return false;
	}
}, '验证起缴日期');

//验证起缴日期要小于结束日期
jQuery.validator.addMethod('isTimeLess', function (value) {
	time_s=$('.time_start').val();
	time_s=time_s.split('.');
	year_s=parseInt(time_s[0]);
	month_s=parseInt(time_s[1]);

	time_e=$('.time_end').val();
	time_e=time_e.split('.');
	year_e=parseInt(time_e[0]);
	month_e=parseInt(time_e[1]);

	var myDate = new Date();
	var year=myDate.getFullYear();
	var month=myDate.getMonth()+1;
	if(year_s>year||(year_s==year&&month_s>=month))
	{
		if(year_e>year_s||(year_s==year_e&&month_e>=month_s))
		{

			return true;
		}else
		{
			return false;
		}
	}else
	{
		return false;
	}

}, '验证起缴日期要小于结束日期');



//验证日期是不是超过12下个月
jQuery.validator.addMethod('isTimeBig12', function (value) {
	time_s=$('.time_start').val();
	time_s=time_s.split('.');
	year_s=parseInt(time_s[0]);
	month_s=parseInt(time_s[1]);

	time_e=$('.time_end').val();
	time_e=time_e.split('.');
	year_e=parseInt(time_e[0]);
	month_e=parseInt(time_e[1]);

	var myDate = new Date();
	var year=myDate.getFullYear();
	var month=myDate.getMonth()+1;
	if(year_s>year||(year_s==year&&month_s>=month))
	{
		  if(year_e>year_s||(year_s==year_e&&month_e>=month_s))
		  {

				if(year_s<year_e)
				{
					month_num=(12-month_s)+month_e;
					if(month_num>10)
					{
						return false;
					}else
					{

						return true;
					}

				}else
				{
					return true;
				}
		  }else
		  {

			  return false;
		  }

	}else
	{
		return false;
	}


}, '验证日期是不是超过12下个月');




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

//获取基数范围提示
function getTimeBigAlert(){
	return "提示：起缴日期要大于等于当前日期";

}
function getTimeLessAlert(){
	return "提示：日期要小于结束日期";

}

function getTime12Alert(){
	return "提示：日期不可以超过12个月";

}

//表单验证
$("#form-data").validate({
	onfocusout: function(element){
        $(element).valid();
    },
	errorElement: 'em',
	invalidHandler: function(form, validator) {//validate只显示第一个警告
        $.each(validator.invalid,function(key,value){
        	if($("span[for='"+key+"']").length >0 ){
        		return false;
        	}
        	$("[name='"+key+"']").after("<span for='"+key+"' class='hint'>"+value+"</span>");
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
			isTimeBig:true,
			//isTimeLess:true,
			//isTimeBig12:true

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
		},
		social_type:{
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
			required:"提示：请选择起缴月份",
			isTimeBig:getTimeBigAlert(),
			//isTimeLess:getTimeLessAlert(),
			//isTimeBig12:getTime12Alert(),
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
		},
		social_type:{
			required:"提示：请选择缴纳类型"
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
		$.get("/wechat/social/getsocialprice/?format=json",postStr,function(data){
		    //alert(data.status);
			//console.log(data);
			if(data.recode == 10000){
				alert(1);
				// time_s=$('.time_start').val();
				// time_s=time_s.split('.');
				// year_s=parseInt(time_s[0]);
				// month_s=parseInt(time_s[1]);
                //
				// time_e=$('.time_end').val();
				// time_e=time_e.split('.');
				// year_e=parseInt(time_e[0]);
				// month_e=parseInt(time_e[1]);
				// var myDate = new Date();
				// var year=myDate.getFullYear();
				// var month=myDate.getMonth()+1;
				// if(year_s>year||(year_s==year&&month_s>=month))
				// {
				// 	if(year_s<year_e||(year_s==year_e&&month_s<=month_e))
				// 	{
				// 		month_num=1;
				// 		if(year_s<year_e){
				// 			month_num=12-month_s+month_e;
				// 		}
				// 		if(year_s==year_e){
				// 			month_num=month_e-month_s+1;
				// 		}
				// 	}else
				// 	{
                //
				// 		$('.time_end').val(year_s.toString()+'.'+month_s.toString());
				// 	}
				// }else
				// {
				// 	d_year=year.toString();
				// 	d_month=month.toString();
				// 	$('.time_start').val(d_year+'.'+d_month);
				// }
				// social_basic=parseInt($("#social_basic").val());
				// fund_basic=parseInt($("#fund_basic").val());
				// yg_is_social=parseInt($("#yg_is_social").val());
				// yg_is_fund=parseInt($("#yg_is_fund").val());
                //
				// var yanglao=(data.data.endowment*social_basic*yg_is_social).toFixed(2);
				// 	$(".yanglao").text((data.data.endowment*social_basic*yg_is_social).toFixed(2));
				// var yiliao=(data.data.medical*social_basic*yg_is_social).toFixed(2);
				// 	$(".yiliao").text((data.data.medical*social_basic*yg_is_social).toFixed(2));
				// var shiye=(data.data.unemployment*social_basic*yg_is_social).toFixed(2);
				// 	$(".shiye").text((data.data.unemployment*social_basic*yg_is_social).toFixed(2));
				// var gongshang=(data.data.employment*social_basic*yg_is_social).toFixed(2)
				// 	$(".gongshang").text((data.data.employment*social_basic*yg_is_social).toFixed(2));
				// var shengyu=(data.data.maternity*social_basic*yg_is_social).toFixed(2)
				// 	$(".shengyu").text((data.data.maternity*social_basic*yg_is_social).toFixed(2));
				// var canzhangjin=(data.data.disability*yg_is_social).toFixed(2);
				// 	$(".canzhangjin").text((data.data.disability*yg_is_social).toFixed(2));
				// var gongjijin=(data.data.housingfund*fund_basic*yg_is_fund).toFixed(2);
				// 	$(".gongjijin").text((data.data.housingfund*fund_basic*yg_is_fund).toFixed(2));
				// $(".month_num").text((month_num*(yg_is_fund||yg_is_social)));
				// var fuwu=30*(month_num*(yg_is_fund||yg_is_social))+10;
				// 	$(".fuwu").text(30*(month_num*(yg_is_fund||yg_is_social))+10);
				// all_money=parseFloat(yanglao,2)+
				// 	parseFloat(yiliao,2)+
				// 	parseFloat(shiye,2)+
				// 	parseFloat(gongshang,2)+
				// 	parseFloat(shengyu,2)+
				// 	parseFloat(canzhangjin,2)+
				// 	parseFloat(gongjijin,2)+
				// 	parseFloat(fuwu,2);
				// all_money=all_money.toFixed(2);
				// $("#all_money").html(all_money+"元");
			}else{
				//alert(data.info);
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