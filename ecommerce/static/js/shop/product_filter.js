$(document).ready(function(){
	$(".ajaxLoader").hide();
	// Product Filter Start
	$(".filter-checkbox").on('click',function(){
		let _filterObj={};
		// var _minPrice=$('#maxPrice').attr('min');
		// var _maxPrice=$('#maxPrice').val();
		// _filterObj.minPrice=_minPrice;
		// _filterObj.maxPrice=_maxPrice;
		$(".filter-checkbox").each(function(index,ele){
            let slug = $("[name='slug']").val();
			let _filterVal=$(this).val();
			let _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
            data = {
                "_filterObj": _filterObj,
                "slug": slug,
            }
            console.log(data)
		});

		// Run Ajax
		$.ajax({
			url:'/filter-data',
			data: data,
			dataType:'json',
			beforeSend:function(){
				$(".ajaxLoader").show();
			},
			success:function(res){
				console.log(res);
				$("#filteredProducts").html(res.data);
				$(".ajaxLoader").hide();
			}
		});
	});
	// End

	// Filter Product According to the price
	// $("#maxPrice").on('blur',function(){
	// 	var _min=$(this).attr('min');
	// 	var _max=$(this).attr('max');
	// 	var _value=$(this).val();
	// 	console.log(_value,_min,_max);
	// 	if(_value < parseInt(_min) || _value > parseInt(_max)){
	// 		alert('Values should be '+_min+'-'+_max);
	// 		$(this).val(_min);
	// 		$(this).focus();
	// 		$("#rangeInput").val(_min);
	// 		return false;
	// 	}
	// });
	// End
});