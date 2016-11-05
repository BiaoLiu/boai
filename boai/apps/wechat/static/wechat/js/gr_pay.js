//全选
$("#check_all").click(function(){
	$(this).parent("label").toggleClass("off");
	if($(this).is(":checked")){
		$(".bill_id").prop("checked",true);
		$(".bill_id").parent("label").removeClass("off");
		$(".bill_id").parents(".row").removeClass('uncheck');
	}else{
		$(".bill_id:enabled").each(function(){
			$(this).prop("checked",false);
			$(this).parent("label").addClass("off");
			$(this).parents(".row").addClass('uncheck');
		});
	}
	calculateTotal();
});

//单选
$(".bill_id").click(function(){
	$(this).parent("label").toggleClass("off");
	$(this).parents(".row").toggleClass("uncheck");
	if(!$(this).is(":checked")){
		$("#check_all").prop("checked",false);
		$("#check_all").parent("label").addClass("off");
	}else{
		if($(".uncheck").length == 0 ) {
			$("#check_all").prop("checked",true);
			$("#check_all").parent("label").removeClass("off");
		}
	}
	calculateTotal();
});


//付款
$("#pay-btn").click(function(){
	if($(this).hasClass("disabled")){
		return false;
	}
	var val = new Array();
	$(".bill_id").each(function() {
		if ($(this).is(":checked")) {
			val.push($(this).val());
		}
	});
	var fp_type = $("#is_piao").is(":checked") ? 'yes' : 'no';
	if (val == '') {
		alert('请选择需要付款的账单');
		return false;
	}
	$(this).addClass("disabled");
	$("#waiting_div").removeClass("hide");
	window.location.href="/GrPay/onPayBank/key/"+val+"_"+fp_type;
});

$(".choose_box").click(function(){
    var fp_type = $("#is_piao").is(":checked") ? 1 : 0;
    var obj = $(this);
    $.post("/GrInfo/setFpType",{fp_type:fp_type},function(r){
        if ( r.status == 1 ) {
            calculateTotal();
            obj.siblings("span").removeClass("active");
            if ( fp_type ) {

                obj.siblings(".open").addClass("active");
                $(".open_msg").removeClass("hide");
                $(".close_msg").addClass("hide");
            } else {
                obj.siblings(".close").addClass("active");
                $(".open_msg").addClass("hide");
                $(".close_msg").removeClass("hide");
            }
        } else {
            alert(r.info);
        }
    },'json');
});

//计算总计
function calculateTotal(){
    var all_money = parseFloat($("#total").attr("tval"));
    $.each($(".bill_id:not(:checked)"),function(){
    	all_money -= parseFloat($(this).attr("tval"));
    });
    if ( $("#is_piao").is(":checked") ) {
        all_money += parseFloat($("#gr_fapiao_fee").val());
    }
    $("#total").text(billMoneyFormat(all_money));
}

function billMoneyFormat (num) {
    return (num.toFixed(2) + '').replace(/\d{1,3}(?=(\d{3})+(\.\d*)?$)/g, '$&,');
}