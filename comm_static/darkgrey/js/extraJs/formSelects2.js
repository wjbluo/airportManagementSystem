(function(layui){
	return window.formSelects2 = formSelects2 = {
		options:{
			layFilter: '',
			left:'【',
			right:'】',
			separator:'',
		},
		$dom: null,
		arr: [],
		on(options){//开启
			if(!options || !options.layFilter){
				alert('请传入lay-filter');
				return ;
			}
			layui.use(['form', 'jquery'], function(){
				var form = layui.form, $ = layui.jquery;
				$.extend(true, formSelects2.options, options);
				formSelects2.$dom = $('select[lay-filter="'+formSelects2.options.layFilter+'"]').next();
				formSelects2.$dom.find('dl').css('display', 'none');
				form.on('select('+formSelects2.options.layFilter+')', function(data){
				  	var $choose = formSelects2.exchange(data);
				  	//如果所选有值, 放到数组中
				  	if($choose){
				  		var include = false;
				  		for(var i in formSelects2.arr){
				  			if(formSelects2.arr[i] && formSelects2.arr[i].val == $choose.val){
				  				formSelects2.arr.splice(i,1);
				  				include = true;
				  			}
				  		}
				  		if(!include){
				  			formSelects2.arr.push($choose);
				  		}
				  	}
				  	//调整渲染的Select显示
				  	formSelects2.show();
				  	//取消收缩效果
					formSelects2.$dom.find('dl').css('display', 'block');
				  	//这行代码是用于展示数据结果的
				  	// formatJson(formSelects.arr);
				});
				
				$(document).on('click', 'select[lay-filter="'+formSelects2.options.layFilter+'"] + div input', ()=>{
					formSelects2.show();
				});
				$(document).on('click', 'body:not(select[lay-filter="'+formSelects2.options.layFilter+'"] + div)', (e)=>{
					var showFlag = $(e.target).parents('.layui-form-select').prev().attr('lay-filter') == formSelects2.options.layFilter;
					var thisFlag = formSelects2.$dom.find('dl').css('display') == 'block';
					if(showFlag){//点击的input框
						formSelects2.$dom.find('dl').css('display', thisFlag ? 'none' : 'block');
					}else{
						if(thisFlag){
							formSelects2.$dom.find('dl').css('display', 'none');
						}
					}
				});
			});
		},
		show(){
		  	formSelects2.$dom.find('.layui-this').removeClass('layui-this');
		  	var input_val = '';
		  	for(var i in formSelects2.arr){
		  		var obj = formSelects2.arr[i];
		  		if(obj){
		  			input_val += formSelects2.options.separator + formSelects2.options.left+obj.name+formSelects2.options.right;
					formSelects2.$dom.find('dd[lay-value="'+obj.val+'"]').addClass('layui-this');
		  		}
		  	}
		  	if(formSelects2.options.separator && formSelects2.options.separator.length > 0 && input_val.startsWith(formSelects2.options.separator)){
		  		input_val = input_val.substr(formSelects2.options.separator.length);
		  	}
		  	formSelects2.$dom.find('.layui-select-title input').val(input_val);
		},
		exchange(data){
			if(data.value){
				return {
					name: $(data.elem).find('option[value='+data.value+']').text(),
					val: data.value
				}
			}
		}
	};
})(layui);
