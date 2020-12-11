$(function () {
  $("a#open_contract_short").bind("click", function () {
    $.getJSON(
      "/open_contract_short",
      {
        position_size: $('input[name="position_size"]').val(),
      },
      function (data) {
        $("#result").text(data.result);
        $("#contract-section").load(" #contract-section > *");
      }
    );
    return false;
  });
});
