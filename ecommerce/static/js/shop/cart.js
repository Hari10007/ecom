
    // $('.increment-item').click(function(event) {
    //     var product_id = $(this).closest('.product-data').find('.prod_id').val();
    //     $.ajax({
    //         data: {
    //             "product_id": product_id,
    //         },
    //         url: "/increment_cart",
    //         //
    //         success: function (response) {
    //             product_id = response.product_id;
    //             quantity = response.quantity;
    //             subtotal = response.subtotal;
    //             total = response.total;
                
    //             $("#quantity-"+product_id).text(quantity);
    //             $("#subtotal-"+product_id).text(subtotal);
    //             $("#total").text(total);
    //         }
    //     });

    //     return false;
    // });

    // $('.decrement-item').click(function(event) {
    //     var product_id = $(this).closest('.product-data').find('.prod_id').val();
    //     $.ajax({
    //         data: {
    //             "product_id": product_id,
    //         },
    //         url: "/decrement_cart",
    //         //
    //         success: function (response) {
    //             product_id = response.product_id;
    //             quantity = response.quantity;
    //             subtotal = response.subtotal;
    //             total = response.total;
                
    //             $("#quantity-"+product_id).text(quantity);
    //             $("#subtotal-"+product_id).text(subtotal);
    //             $("#total").text(total);

    //         }
    //     });

    //     return false;  
    // });


updateBtn = document.getElementsByClassName("update-item")

for(var i=0; i< updateBtn.length; i++){
    updateBtn[i].addEventListener('click',function(){
    var productId = this.dataset.product
    var action = this.dataset.action

    if (action == "add"){
        $.ajax({
            data: {
                "product_id": productId,
            },
            url: "/increment_cart",
            //
            success: function (response) {
                product_id = response.product_id;
                quantity = response.quantity;
                subtotal = response.subtotal;
                total = response.total;

                $("#quantity-"+product_id).text(quantity);
                $("#subtotal-"+product_id).text(subtotal);
                $("#sub_total-"+product_id).text(subtotal);
                $("#total").text(total);
            }
        });
    }
    else{
        $.ajax({
            data: {
                "product_id": productId,
            },
            url: "/decrement_cart",
            //
            success: function (response) {
                product_id = response.product_id;
                quantity = response.quantity;
                subtotal = response.subtotal;
                total = response.total;
                               
                $("#quantity-"+product_id).text(quantity);
                $("#subtotal-"+product_id).text(subtotal);
                $("#sub_total-"+product_id).text(subtotal);
                $("#total").text(total);
                
                if (quantity == 1){
                    document.querySelector('[data-product="{{ product_id } "]').disabled = true;
                    const elements = document.querySelectorAll("data-product");
                    elements.forEach(function (element) {
                        element.disabled = true;
                    });
                }
            }
        });
    }
    })
}