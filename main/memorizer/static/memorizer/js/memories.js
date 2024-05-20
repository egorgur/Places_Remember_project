function createMemoRedirect() {
    const url = baseUrl + "/memorizer/memories/create"
    location.href = url
}

ymaps.ready(init)

function init() {
    let maps = {}
    for (const memoId in memories) {
        const memo = memories[memoId]
        maps[memo.id] = new ymaps.Map("map_" + memo.id, {
            center: [memo["position_x"], memo["position_y"]],
            zoom: 7,
            controls: []
        }, {
            suppressMapOpenBlock: true
        })

        const placemark = createPlacemark([memo.position_x, memo.position_y])
        getAddress(placemark, placemark.geometry.getCoordinates());
        maps[memo.id].geoObjects.add(placemark);
    }

    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    function getAddress(placemark, coords) {
        placemark.properties.set('iconCaption', 'поиск...');
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);

            placemark.properties
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

function redirectToMemo(memoId){
    const url = baseUrl + "/memorizer/memories/" + memoId
    location.href = url
}