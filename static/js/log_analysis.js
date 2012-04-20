$(document).ready(function() {
//       $('#archiv').spinner({img: 'static/img/busy.gif'});
// 	$("#logsButton").live('click', function(){
// 		$.ajax({type:"GET", 
// 				url: "/log_analysis/extractSubjects", 
// 				success: function(data){
//                                         $('#spinner').spinner('remove');
// 					$('#content').html(data);
// 		     		}, 
// 				data: {},
// 		});
// 		$("#content").html('<h3 id="spinner">Právě probíhá analýza logů. Mějte strpení. Může to trvat pěkně dlouho...</h3>');
//                 $('#spinner').spinner({img:'static/img/busy.gif', position: 'left',});
// 	});
         
//         $("#export_button").live('click', function(){
// 		$.ajax({type:"GET", 
// 				url: "/log_analysis/export_data", 
// 				success: function(data){
// //                                         $('#spinner').spinner('remove');
// // 					$('#content').html(data);
// 		     		}, 
// 				data: {},
// 		});
// 		$("#content").html('<h3 id="spinner">Právě probíhá analýza logů. Mějte strpení. Může to trvat pěkně dlouho...</h3>');
//                 $('#spinner').spinner({img:'static/img/busy.gif', position: 'left',});
    $("#subrange_left_input, #subrange_right_input").live("keyup", function(){
        var left_count = $("#subrange_left_input").val().length
        var right_count = $("#subrange_right_input").val().length
        
        if(left_count + right_count > 0){
            $("#regexp_input").attr("disabled", true);
        }
        else{
            $("#regexp_input").removeAttr("disabled");
        }
    });
    
    $("#regexp_input").live("keyup", function(){
        var regexp_count = $(this).val().length
        
        if(regexp_count > 0){
            $("#subrange_left_input, #subrange_right_input").attr("disabled", true);
        }
        else{
            $("#subrange_left_input, #subrange_right_input").removeAttr("disabled");
        }
    });
});
        
        $(".deleteArchive").live('click', function(){
                var parent = $(this).parent('li');
                var archive = $('a', parent).text();
		$.ajax({type:"POST", 
				url: "/log_analysis/deleteArchive", 
				success: function(data){
					parent.hide('slow');
		     		}, 
				data: {archive : archive},
		});
	});