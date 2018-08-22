/*****************************************************************************/
/* TabularEmbed: Event Handlers */
/*****************************************************************************/
Template.TabularEmbed.events({
    'click .copy-code': function(event, template) {
        event.preventDefault();
        // Read the embed code
        var code = $("#"+this._id)[0]["innerText"];
        // Store it in a temporary input and then to the clipboard
        var temporaryInput = $("<input>");
        $("body").append(temporaryInput);
        temporaryInput.val(code).select();
        document.execCommand("copy");
        temporaryInput.remove();
    }
});

/*****************************************************************************/
/* TabularEmbed: Helpers */
/*****************************************************************************/
Template.TabularEmbed.helpers({
    visId: function() {
        return this._id;
    },
    data: function() {
        var url = window.location.href + "vis/" + this._id;
        return '<iframe style="border: none; width: 100%; height: 100%;" src="'+url+'"></iframe>';
    }
});

/*****************************************************************************/
/* TabularEmbed: Lifecycle Hooks */
/*****************************************************************************/
Template.TabularEmbed.onCreated(function () {
});

Template.TabularEmbed.onRendered(function () {
});

Template.TabularEmbed.onDestroyed(function () {
});
