const VKID = window.VKIDSDK;

VKID.Config.set({
  app: VK_APP_ID, // Идентификатор приложения.
  redirectUrl: "https://memorizer.testotheca.online/auth/process", // Адрес для перехода после авторизации.
});

const oneTap = new VKID.OneTap();

// Получение контейнера из разметки.
const container = document.getElementById('VkIdSdkOneTap');

// Проверка наличия кнопки в разметке.
if (container) {
  // Отрисовка кнопки в контейнере с именем приложения APP_NAME, светлой темой и на русском языке.
  oneTap.render({
      container: container,
      scheme: VKID.Scheme.LIGHT,
      lang: VKID.Languages.RUS,
      showAlternativeLogin: true,
  });
}