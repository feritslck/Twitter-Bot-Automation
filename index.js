require('dotenv').config();
const { TwitterApi } = require('twitter-api-v2');
const fs = require('fs');
const cron = require('node-cron');

const path = './tweeted.json';

// Dosya yoksa otomatik oluştur
if (!fs.existsSync(path)) {
  fs.writeFileSync(path, JSON.stringify([]));
  console.log('tweeted.json dosyası oluşturuldu (boş).');
}

const client = new TwitterApi({
  appKey: process.env.API_KEY,
  appSecret: process.env.API_SECRET,
  accessToken: process.env.ACCESS_TOKEN,
  accessSecret: process.env.ACCESS_SECRET,
});

const rwClient = client.readWrite;

function alreadyQuoted(tweetId) {
  const data = JSON.parse(fs.readFileSync(path));
  return data.includes(tweetId);
}

function saveQuoted(tweetId) {
  const data = JSON.parse(fs.readFileSync(path));
  data.push(tweetId);
  fs.writeFileSync(path, JSON.stringify(data));
  console.log('Tweet ID kaydedildi:', tweetId);
}

function getTweetCount() {
  const data = JSON.parse(fs.readFileSync(path));
  return data.length;
}

async function checkAndQuoteTweet() {
  try {
    console.log('Fonksiyon tetiklendi');

    // Kullanıcı adından ID’yi çek
    const user = await client.v2.userByUsername(process.env.TARGET_USERNAME);
    const userId = user.data.id;
    const username = user.data.username;

    console.log('Kullanıcı adı:', username);
    console.log('Kullanıcı ID:', userId);

    const response = await client.v2.userTimeline(userId, {
      max_results: 5,
      'tweet.fields': ['id', 'text', 'created_at']
    });

    const tweets = response.data?.data || response.data || [];
    console.log('Gelen tweet sayısı:', tweets.length);

    if (!Array.isArray(tweets) || tweets.length === 0) {
      console.log('Hiç tweet bulunamadı.');
      return;
    }

    for (const tweet of tweets) {
      const tweetId = tweet.id;
      if (alreadyQuoted(tweetId)) {
        console.log('Zaten alıntılandı:', tweetId);
        continue;
      }

      const tweetUrl = `https://x.com/${username}/status/${tweetId}`;
      const count = getTweetCount() + 1;
      const fullText = `${process.env.QUOTE_TEXT} #${count}\n\n${tweetUrl}`;

      await rwClient.v2.tweet({ text: fullText });
      saveQuoted(tweetId);
      console.log('Alıntı tweet atıldı:', tweetUrl);
      break;
    }
  } catch (err) {
    console.error('Hata:', err);
  }
}

// İlk çalıştırma
(async () => {
  await checkAndQuoteTweet();
})();

// Her 2 günde 1 sabah 10:00'da otomatik çalışır
cron.schedule('0 10 */2 * *', () => {
  console.log('Zamanlayıcı tetiklendi');
  checkAndQuoteTweet();
});