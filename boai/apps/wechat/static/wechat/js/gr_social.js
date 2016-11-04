//当前日期
var c_date = new Date();
var c_year =c_date.getFullYear();
var c_month=c_date.getMonth()+1;
//获取时间戳
function get_unix_time(dateStr)
{
    var newstr = dateStr.replace(/-/g,'/');
    var date =  new Date(newstr);
    var time_str = date.getTime().toString();
    return parseInt(time_str.substr(0, 10));
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

//验证当前日期是否超过本月20号
jQuery.validator.addMethod('isTimeBig20', function (value) {
	//所选月的20号
	var this_month_20=get_unix_time(value+'-20');
	//现在时间戳
	var time_now = Date.parse(new Date())/1000;
	if(time_now>=this_month_20)
	{
		return false;
	}else
	{
		return true;
	}
}, '验证当前日期是否超过本月20号');

//验证当前日期是否大于等于当前日期且小于结束日期
jQuery.validator.addMethod('isTimeBigNow', function (value) {
	var every_year_month=get_unix_time(c_year+'-'+c_month);
	var time_start=get_unix_time(value);
	var time_end=get_unix_time($('.time_end').val());
	if(time_start<every_year_month||time_start>time_end)
	{
		return false;
	}else
	{
		return true;
	}
}, '验证当前日期是否大于等于当前日期且小于结束日期');

//验证日期是不是超过12下个月
jQuery.validator.addMethod('isTimeBig12', function (value) {
	var time_start=get_unix_time(value);
	var time_end=get_unix_time($('.time_end').val());
	if((time_end-time_start)>12*30*24*3600)
	{
		return false;
	}else
	{
		return true;
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
//日期提交
$("input[type='month']").blur(function(){
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
	return "提示：时间必须大于等于当前时间且小于结束时间";

}
function getTimeBig20Alert(){
	return "提示：本月已过20号，请选择下一月社保";

}

function getTime12Alert(){
	return "提示：日期不可以超过12个月";

}

//表单验证

$("#form-data").validate({
	errorElement: 'em',
	invalidHandler: function(form, validator) {
		//validate只显示第一个警告
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
			isTimeBigNow:true,
			isTimeBig20:true,
			isTimeBig12:true,

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
			isTimeBigNow:getTimeBigAlert(),
			isTimeBig20:getTimeBig20Alert(),
			isTimeBig12:getTime12Alert()
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
			if(data.recode == 10000)
			{
				//社保基数
				social_basic=parseInt($("#social_basic").val());
				//公积金基数
				fund_basic=parseInt($("#fund_basic").val());
				//是否缴纳社保
				yg_is_social=parseInt($("#yg_is_social").val());
				//是否缴纳公积金
				yg_is_fund=parseInt($("#yg_is_fund").val());
				//开始时间
				var time_start=get_unix_time($('.time_start').val());
				//结束时间
				var time_end=get_unix_time($('.time_end').val());
				//时间差
				common=time_end-time_start;
				year = Math.floor(common/86400/360);    //整数年
  				month_num = Math.floor(common/86400/30) - year*12+1; //整数月

				var yanglao=(data.data.endowment*social_basic*yg_is_social).toFixed(2);
				$(".yanglao").text((data.data.endowment*social_basic*yg_is_social).toFixed(2));
				var yiliao=(data.data.medical*social_basic*yg_is_social).toFixed(2);
				$(".yiliao").text((data.data.medical*social_basic*yg_is_social).toFixed(2));
				var shiye=(data.data.unemployment*social_basic*yg_is_social).toFixed(2);
				$(".shiye").text((data.data.unemployment*social_basic*yg_is_social).toFixed(2));
				var gongshang=(data.data.employment*social_basic*yg_is_social).toFixed(2)
				$(".gongshang").text((data.data.employment*social_basic*yg_is_social).toFixed(2));
				var shengyu=(data.data.maternity*social_basic*yg_is_social).toFixed(2)
				$(".shengyu").text((data.data.maternity*social_basic*yg_is_social).toFixed(2));
				var canzhangjin=(data.data.disability*yg_is_social).toFixed(2);
				$(".canzhangjin").text((data.data.disability*yg_is_social).toFixed(2));
				var gongjijin=(data.data.housingfund*fund_basic*yg_is_fund).toFixed(2);
				$(".gongjijin").text((data.data.housingfund*fund_basic*yg_is_fund).toFixed(2));
				$(".month_num").text((month_num*(yg_is_fund||yg_is_social)));
				var fuwu=30*(month_num*(yg_is_fund||yg_is_social))+10;
				$(".fuwu").text(30*(month_num*(yg_is_fund||yg_is_social))+10);
				all_money=parseFloat(yanglao,2)+ parseFloat(yiliao,2)+ parseFloat(shiye,2)+
				 	parseFloat(gongshang,2)+
				 	parseFloat(shengyu,2)+
				 	parseFloat(canzhangjin,2)+
				 	parseFloat(gongjijin,2)+
				 	parseFloat(fuwu,2);
				 all_money=all_money.toFixed(2);
				 $("#all_money").html(all_money+"元");
			}else
			{

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
	//社保基数
	social_type=$('.social_type').val();
	social_basic=parseInt($("#social_basic").val());
	//公积金基数
	fund_basic=parseInt($("#fund_basic").val());
	//是否缴纳社保
	yg_is_social=parseInt($("#yg_is_social").val());
	//是否缴纳公积金
	yg_is_fund=parseInt($("#yg_is_fund").val());
	//开始时间
	var time_start=$('.time_start').val();
	//结束时间
	var time_end=$('.time_end').val();
	
	post_data={
		social_type:social_type,
		is_social:yg_is_social,
		is_fund:yg_is_fund,
		social_base:social_basic,
		fund_base:fund_basic,
		startmonth:time_start,
		endmonth:time_end,
	}
	$.post("/wechat/wuxian/",post_data,function(data){
		if(data.status == 1){
			window.location.href="/GrPay/index";
		}else if(data.status == 2){
			console.log(data);
			window.location.href="/GrPay/unpayedOrder/";
		}else{
			console.log(data);
		}
	},'json');
})

if(is_show == 1){
    modal('save','show');
}