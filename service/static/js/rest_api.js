$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#pet_id").val(res.id);
        $("#pet_name").val(res.productId);
        $("#pet_category").val(res.suggestionId);
        $("#pet_available").val(res.categoryId);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#pet_name").val("");
        $("#pet_category").val("");
        $("#pet_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Pet
    // ****************************************

    $("#create-btn").click(function () {

        var productId = $("#pet_name").val();
        var suggestionId = $("#pet_category").val();
        var categoryId = $("#pet_available").val()

        var data = {
            "productId": productId,
            "suggestionId": suggestionId,
            "categoryId": categoryId
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Pet
    // ****************************************

    $("#update-btn").click(function () {

        var id = $("#pet_id").val();
        //var productId = $("#pet_name").val();
        //var suggestionId = $("#pet_category").val();
        var categoryId = $("#pet_available").val() ;

        var data = {
        //    "productId": productId,
        //    "suggestionId": suggestionId,
            "categoryId": categoryId
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/" + id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Pet
    // ****************************************

    $("#retrieve-btn").click(function () {

        var id = $("#pet_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations/" + id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Pet
    // ****************************************

    $("#delete-btn").click(function () {

        var id = $("#pet_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/recommendations/" + id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Pet with ID [" + res.id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // perform action
    // ****************************************
    $("#action-btn").click(function () {

        var id = $("#pet_id").val();
        var categoryId = $("#pet_available").val() ;

        var data = {
            "categoryId": categoryId
        };



        var ajax = $.ajax({
                type: "PUT",
                url: "/recommendations/category/" + id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#pet_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Pet
    // ****************************************

    $("#search-btn").click(function () {

        var productId = $("#pet_name").val();
        var suggestionId = $("#pet_category").val();
        var categoryId = $("#pet_available").val() == "true";

        var queryString = ""

        if (productId) {
            queryString += 'name=' + productId
        }
        if (suggestionId) {
            if (queryString.length > 0) {
                queryString += '&category=' + suggestionId
            } else {
                queryString += 'category=' + suggestionId
            }
        }
        if (categoryId) {
            if (queryString.length > 0) {
                queryString += '&available=' + categoryId
            } else {
                queryString += 'available=' + categoryId
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/recommendations?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">ProductId</th>'
            header += '<th style="width:40%">suggestionId</th>'
            header += '<th style="width:10%">categoryId</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                recommendation = res[i];
                var row = "<tr><td>"+recommendation._id+"</td><td>"+recommendation.productId+"</td><td>"+recommendation.suggestionId+"</td><td>"+recommendation.categoryId+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
