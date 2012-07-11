$(document).ready(function() {

    set_original_values();
    store_updated_rows(true);

    $("td").on("click", "#id_category", function(){
        var option = $(this).val();
        update_category($(this), option);
    });

    $("td").on("click", "#id_subject_category", function(){
        var option = $(this).val();
        update_subject_category($(this), option);
    });

    $("#data_edit").on("click", "tr", function(){
        $(this).addClass("updated");
        $(this).addClass("changed");
    });

    $(window).unload( function () {
        console.log("ok");
        store_updated_rows("changed", false);  
    });

});

function store_updated_rows(select_class, async){
    if(async == null){
        async = true
    }

    if(select_class == null){
        select_class = "updated"
    }

    $("." + select_class).each(function(index, tr){
        var subject = $(tr).find(".subject").text();
        var category = $(tr).find("#id_category").val();
        var subject_category = $(tr).find("#id_subject_category").val();
        var acquisition = $(tr).find("#id_acquisition").attr("checked");
        var note = $(tr).find("#id_note").val();

        $.ajax({
            type: 'POST',
            url: "store_updated_row",
            async: async,
            data: {subject: subject, subject_category: subject_category, category: category, acquisition:acquisition, note:note},
            success: function(msg){
                $(tr).removeClass("updated");
            }
        });
    });
    
    setTimeout(store_updated_rows, 60000);
}

    function set_original_values(){
        $(".processed").each(function(index, tr){
            var category = $(tr).find(".category").attr("data-original");
            var current_select = $(tr).find("#id_category");
            update_category(current_select, category);

            if(category == 4){
                 var subject_category = $(tr).find(".subject_category").attr("data-original");
                 var current_select = $(tr).find("#id_subject_category");
                 update_subject_category(current_select, subject_category);
            }

            var note = $(tr).find(".note").attr("data-original");
            $(tr).find("#id_note").val(note);

            var acquisition = $(tr).find(".acquisition").attr("data-original");
            if(acquisition == "True"){
                $(tr).find("#id_acquisition").attr("checked", "true");
            }

        });
    }

    function update_category(current_select, option){
        current_select.val(option);
        var td = current_select.parent("td").next();
        var tr = td.parent("tr");
        var subject_category = td.find("#id_subject_category");
        
        if(option == 4){ 
            subject_category.removeAttr("disabled");
            td.attr("class", "active subject_category");
            tr.attr("class", "neutral");
        }
        else{
            subject_category.attr("disabled", "disabled");
            subject_category.val(0);
            td.attr("class", "disabled subject_category");
            tr.attr("class", "denied");
        }
    }

    function update_subject_category(current_select, option){
        current_select.val(option);
        var tr = current_select.parent("td").parent("tr");
        // var subject_category = td.find("#id_subject_category");
        
        if(option == 1|option == 2){
            tr.attr("class", "accepted");
        }
        else if(option == 0){
            tr.attr("class", "");
        }
        else{
            tr.attr("class", "denied");
        }
    }