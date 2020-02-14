function Ingredient(data) {
    return {
    name: data["name"],
    applicableTags: ko.observableArray(data["tags"])
    };
}

function IngredientTags() {
    var that = this;
    var allTags = JSON.parse(document.getElementById('tags-data').textContent);
    var allIngredients = JSON.parse(document.getElementById('ingredients-data').textContent);

    this.ingredients = ko.observableArray(allIngredients.map((x) => Ingredient(x)));
    this.tags = ko.observableArray(allTags);

    ko.computed(function() {
        return ko.toJSON(this.ingredients);
    }).subscribe(this.assignTags)

    this.assignTags = function(data, event) {
        console.debug(data)
        var url = $(event.target).data("url");
        var csrftoken = Cookies.get('csrftoken');
        $.ajax(url, {
            data: ko.toJSON(data["ingredients"]),
            contentType: 'application/json',
            headers: {
                "X-CSRFToken": csrftoken
            },
            type: 'POST',
            dataType: "json"
        });
    };
}

