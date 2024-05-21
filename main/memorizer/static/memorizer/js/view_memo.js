const nameInput = document.getElementById("name")
const commentInput = document.getElementById("comment")
const mapDiv = document.getElementById("map")
const mapInfo = document.getElementById("mapInfo")


let PlaceMarkCoordinates = {
    x: position_x,
    y: position_y,
}


ymaps.ready(init);

function parceCoordinates(coords) {
    PlaceMarkCoordinates.x = coords[0];
    PlaceMarkCoordinates.y = coords[1];
}

// Code is copied from https://yandex.ru/dev/maps/jsbox/2.1/event_reverse_geocode/
function init() {
    var myMap = new ymaps.Map('map', {
        center: [position_x, position_y],
        zoom: 9,
        controls: [],
    }, {
        searchControlProvider: 'yandex#search',
        suppressMapOpenBlock: true,
    });

    var myPlacemark = createPlacemark([position_x,position_y])
    myMap.geoObjects.add(myPlacemark);
    myPlacemark.events.add('dragend', function (e) {
                getAddress(myPlacemark.geometry.getCoordinates());
                parceCoordinates(myPlacemark.geometry.getCoordinates())
                console.log(PlaceMarkCoordinates)
            });
    getAddress(myPlacemark.geometry.getCoordinates());

    // Слушаем клик на карте.
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
                parceCoordinates(coords)
                console.log(PlaceMarkCoordinates)
            });
        }
        getAddress(myPlacemark.geometry.getCoordinates());
        parceCoordinates(coords)
        console.log(PlaceMarkCoordinates)
    });


    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        myPlacemark.properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);

            myPlacemark.properties
                .set({
                    // Формируем строку с данными об объекте.
                    iconCaption: [
                        // Название населенного пункта или вышестоящее административно-территориальное образование.
                        firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                        // Получаем путь до топонима, если метод вернул null, запрашиваем наименование здания.
                        firstGeoObject.getThoroughfare() || firstGeoObject.getPremise()
                    ].filter(Boolean).join(', '),
                    // В качестве контента балуна задаем строку с адресом объекта.
                    balloonContent: firstGeoObject.getAddressLine()
                });
        });
    }
}

nameInput.addEventListener("input", () => {
    nameInput.style.outline = "none"
})

function mainPageRedirect() {
    const url = baseUrl + "/memorizer/memories"
    location.href = url
}

function sendForm() {
    const x = PlaceMarkCoordinates.x
    const y = PlaceMarkCoordinates.y
    const name = nameInput.value
    const comment = commentInput.value
    if ((x === null || y === null)) {
        mapInfo.classList.add("active")
        mapInfo.innerHTML = "Выберите точку на карте"
    } else {
        mapInfo.classList.remove("active")
        mapInfo.innerHTML = ""
    }
    if (name === "") {
        nameInput.style.outline = "red 1px solid"
    } else {
        nameInput.style.outline = "none"
    }
    console.log((x !== null && y !== null) && (name !== ""))
    if ((x !== null && y !== null) && (name !== "")) {
        const url = window.location.href
        let form = new FormData()

        form.append("name", name)
        form.append("comment", comment)
        form.append("position", JSON.stringify(PlaceMarkCoordinates))

        for (const pair of form.entries()) {
            console.log(pair[0] + ', ' + pair[1]);
        }
        sendRequest("POST", url, form)
            .then(data => {
                console.log(data)
                if (data["success"]) {
                    mainPageRedirect()
                }
            })
            .catch(err => {
                console.log(err)
            })

    }
}
