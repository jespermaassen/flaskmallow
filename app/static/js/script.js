// Open Long Contract
$(function () {
  $("a#open_contract_long").bind("click", function () {
    $.ajax({
      url: "/exchange/open",
      type: "POST",
      data: {
        size: $('input[name="position_size"]').val(),
        market: $("#selectedmarket").val(),
        contract_type: "long",
        action: "open",
      },
      dataType: "json",
      success: function (data) {
        $("#contract-section").load(" #contract-section > *");
      },
    });
    return false;
  });
});
