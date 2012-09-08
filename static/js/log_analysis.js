$(document).ready(function() {

    set_original_values();
    store_updated_rows(true);
    // $("#date_from").datepicker();
    // $('#data_edit').dataTable();

    $("#id_filter_category").multiselect({checkAllText: "Označ vše", uncheckAllText: "Odznač vše", noneSelectedText: "Kategorie", show: ["slide", 100], 
        position: {
        my: 'center',
        at: 'center'}, height: "auto", selectedText: "#", classes: "filter_category"});

    $("#id_filter_subject_category").multiselect({checkAllText: "Označ vše", uncheckAllText: "Odznač vše", noneSelectedText: "Podkategorie", show: ["slide", 100], 
        position: {
        my: 'center',
        at: 'center'}, height: "auto", selectedText: "#", classes: "filter_subject_category"});

    set_original_filter_values();

    $("table").on("click", "#id_category", function(){
        var option = $(this).val();
        update_category($(this), option);
    });

    $("#data_edit").on("click", "#id_subject_category", function(){
        var option = $(this).val();
        update_subject_category($(this), option);
    });

    $("#data_edit").on("click", "tr", function(){
        $(this).addClass("updated");
        $(this).addClass("changed");
    });

    $("#data_edit").on("click", "textarea", function(){
        $(this).autosize();
    });

    $(window).unload(function(){
        store_updated_rows("changed", false);  
    });


    $("#next_page.active").click(function(){
        var number = parseInt($("#page_number").val()) + 1;
        $("#page_number").val(number);
        $("#filter_form").submit();
    });

    $("#previous_page.active").click(function(){
        var number = parseInt($("#page_number").val()) - 1;
        $("#page_number").val(number);
        $("#filter_form").submit();
    });

    $("#set_filters").click(function(){
        $("#page_number").val(0);
        $("#filter_form").submit();
    });

    // $("#hide_processed").bind("click", function(){
    //     var state = $(this).attr("data-state");
    //     if(state == "on"){
    //         $(".processed").hide("fast");
    //         $(this).attr("data-state", "off");
    //         $(this).text("Ukaž zpracované");
    //     }
    //     else{
    //         $(".processed").show("fast");
    //         $(this).attr("data-state", "on");
    //         $(this).text("Schovej zpracované");
    //     }
    // });


    $('.resized textarea').autosize();

    // $(".changeable").change(function(){
    //     $(".active").attr("class", "inactive");
    //     $("#next_page.active").unbind("click");
    // });

});

function set_original_filter_values(){    
    var categories = $("#filter_category").attr("data-original").split(";");
    var subject_categories = $("#filter_subject_category").attr("data-original").split(";");
    var option;

    for(var i in categories){
        option = $(".filter_category").multiselect("widget").find("input[value=" + categories[i] + "]")
            .attr('checked',true)
            .click()
            .attr('checked',true);
    };

    for(var i in subject_categories){
        option = $(".filter_subject_category").multiselect("widget").find("input[value=" + subject_categories[i] + "]")
            .attr('checked',true)
            .click()
            .attr('checked',true);
    };

    var hide_processed = $(".hide_processed").attr("data-original");
    if(hide_processed == "on"){
        $("#id_hide_processed").attr("checked", "true");
    }


    
}

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
        $(".processed, #data_filter tr").each(function(index, tr){
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
            if(acquisition == "1"){
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
            tr.addClass("neutral");
        }
        else if(option == "None"|option == 0){
            tr.removeClass("neutral");
            tr.removeClass("accepted");
            tr.removeClass("denied");
            subject_category.attr("disabled", "disabled");
            // update_subject_category($("#id_subject_category"), 0)
        }
        else{
            subject_category.attr("disabled", "disabled");
            subject_category.val(0);
            td.addClass("disabled");
            tr.addClass("denied");
        }
    }

    function update_subject_category(current_select, option){
        current_select.val(option);
        var tr = current_select.parent("td").parent("tr");
        
        if(option == 1|option == 2){
            tr.removeClass("neutral");
            tr.removeClass("denied");
            tr.addClass("accepted");
        }
        else if(option == 11){
            tr.removeClass("neutral");
            tr.removeClass("denied");
            tr.addClass("psh_descriptor");
        }
        else if(option == 12){
            tr.removeClass("neutral");
            tr.removeClass("denied");
            tr.addClass("psh_nondescriptor");
        }
        else if(option == "None"|option == 0){
            tr.addClass("neutral");
        }
        else{
            tr.removeClass("neutral");
            tr.removeClass("accepted");
            tr.addClass("denied");
        }
    }