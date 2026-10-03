document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Stomach Visualizer Logic
    const stomachTabs = document.querySelectorAll('.stomach-controls .btn-tab');
    const stomachCircle = document.querySelector('.stomach-circle');
    const sizeLabel = document.querySelector('.size-label');
    const capacityLabel = document.querySelector('.capacity-label');
    const stomachInfoTitle = document.querySelector('.stomach-info h3');
    const stomachInfoDesc = document.querySelector('.stomach-info p');
    
    const stomachData = {
        'day1': {
            size: '22px',
            label: 'एक छोटी चेरी (Cherry) के बराबर 🍒',
            capacity: 'क्षमता: 5 से 7 मिलीलीटर (लगभग 1 छोटी चम्मच)',
            title: 'पहले दिन बच्चे का पेट बहुत छोटा होता है!',
            desc: 'जन्म के पहले दिन बच्चे का पेट एक छोटी चेरी जैसा नन्हा होता है। इसमें केवल मां का पहला गाढ़ा पीला दूध (कोलोस्ट्रम) ही समा सकता है, जो कि बच्चे के लिए अमृत और पहली वैक्सीन है। गाय या भैंस का दूध (जो कि 100-200ml की कटोरी में दिया जाता है) इस नन्हे पेट को फैला देता है और नुकसान पहुंचाता है।'
        },
        'day3': {
            size: '50px',
            label: 'एक अखरोट (Walnut) के बराबर 🥜',
            capacity: 'क्षमता: 22 से 27 मिलीलीटर (लगभग 5 छोटी चम्मच)',
            title: 'तीसरे से पांचवें दिन का नन्हा पेट',
            desc: 'अब पेट का आकार थोड़ा बढ़कर अखरोट जितना हुआ है। अभी भी इसमें बहुत कम जगह है। मां का दूध अब पूरी मात्रा में आने लगता है जो इस पेट के लिए एकदम सही है। भैंस या गाय का भारी दूध इस समय देने से बच्चे को भयंकर गैस, उल्टी और पेट दर्द हो सकता है।'
        },
        'month1': {
            size: '95px',
            label: 'एक बड़े अंडे (Egg) के बराबर 🥚',
            capacity: 'क्षमता: 80 से 150 मिलीलीटर',
            title: 'एक महीने का पेट - अभी भी नाजुक',
            desc: 'एक महीने का होने पर भी बच्चे का पेट सिर्फ एक अंडे जितना ही बड़ा होता है। इसके पाचक एंजाइम (digestive enzymes) अभी भी गाय/भैंस के दूध में मौजूद जटिल प्रोटीन (Casein) को पचाने के लिए तैयार नहीं हैं। मां का दूध आसानी से पच जाता है और 2 घंटे में पेट खाली हो जाता है।'
        },
        'month6': {
            size: '140px',
            label: 'एक मौसंबी या सॉफ्टबॉल के बराबर 🍊',
            capacity: 'क्षमता: 150 से 250 मिलीलीटर',
            title: '6 महीने के बाद - धीरे-धीरे बदलाव',
            desc: '6 महीने के बाद बच्चे का पेट ठोस आहार (solid food) और कुछ मात्रा में पानी पचाने लायक होता है। लेकिन ध्यान रहे, मुख्य आहार अभी भी मां का दूध ही रहेगा। 1 साल का होने तक गाय या भैंस का दूध पीने के लिए मना किया जाता है क्योंकि यह अभी भी आंतों को नुकसान पहुंचा सकता है।'
        }
    };

    stomachTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all
            stomachTabs.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked
            tab.classList.add('active');
            
            const ageKey = tab.dataset.age;
            const data = stomachData[ageKey];
            
            // Update Stomach Circle style
            stomachCircle.style.width = data.size;
            stomachCircle.style.height = data.size;
            
            // Update Text content
            sizeLabel.textContent = data.label;
            capacityLabel.textContent = data.capacity;
            stomachInfoTitle.textContent = data.title;
            stomachInfoDesc.textContent = data.desc;
        });
    });

    // 2. Milk Comparison Tabs Logic
    const milkTabs = document.querySelectorAll('.tab-milk');
    const milkPanels = document.querySelectorAll('.comparison-panel');

    milkTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            milkTabs.forEach(btn => btn.classList.remove('active'));
            milkPanels.forEach(panel => panel.classList.remove('active'));
            
            tab.classList.add('active');
            const targetId = tab.dataset.target;
            document.getElementById(targetId).classList.add('active');
        });
    });

    // 3. Accordion Logic (Q&A)
    const accordionHeaders = document.querySelectorAll('.accordion-header');

    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            const isActive = item.classList.contains('active');
            
            // Close all active items
            document.querySelectorAll('.accordion-item').forEach(accItem => {
                accItem.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // 4. Safe Milk Calculator Logic
    const calcForm = document.getElementById('milkCalcForm');
    const calcResultBox = document.getElementById('calcResultBox');
    const resultBadge = calcResultBox.querySelector('.result-badge');
    const resultTitle = calcResultBox.querySelector('.result-title');
    const resultDesc = calcResultBox.querySelector('.result-desc');
    const resultTipsList = calcResultBox.querySelector('.result-tips-list');

    calcForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const ageSelect = document.getElementById('babyAge').value;
        let badgeText = '';
        let badgeClass = '';
        let title = '';
        let desc = '';
        let tips = [];

        if (ageSelect === 'under6m') {
            badgeText = '🚨 केवल मां का दूध (या फॉर्मूला)';
            badgeClass = 'badge-red';
            title = 'गाय या भैंस का दूध बिल्कुल बंद!';
            desc = '0 से 6 महीने के बच्चे के लिए गाय या भैंस का दूध जहर समान भारी हो सकता है। इस उम्र में बच्चे को पानी की भी जरूरत नहीं होती, मां के दूध में 88% पानी और सारे जरूरी पोषक तत्व होते हैं। बाहरी दूध देने से बच्चे को दस्त, निमोनिया और कुपोषण का खतरा 10 गुना बढ़ जाता है।';
            tips = [
                'मां का पहला पीला दूध (कोलोस्ट्रम) जरूर पिलाएं।',
                'दिन-रात मिलाकर 24 घंटे में 8 से 12 बार स्तनपान कराएं।',
                'अगर मां का दूध न आ रहा हो, तो सिर्फ डॉक्टर की सलाह पर शिशु फॉर्मूला (Infant Formula) दें, साधारण दूध नहीं।'
            ];
        } else if (ageSelect === '6to12m') {
            badgeText = '⚠️ मां का दूध + ठोस आहार';
            badgeClass = 'badge-yellow';
            title = 'जानवरों का दूध अभी भी न दें';
            desc = '6 से 12 महीने के बच्चे को ऊपर का खाना (जैसे दाल का पानी, मसला हुआ केला, सूजी की खीर) देना शुरू करना चाहिए, लेकिन पीने के लिए अभी भी गाय या भैंस का दूध नहीं देना है। उनके पेट और गुर्दे (kidneys) अभी भी इतने परिपक्व नहीं हुए हैं कि वे जानवर के दूध को आसानी से संभाल सकें।';
            tips = [
                'कटोरी-चम्मच से मसला हुआ घर का बना खाना खिलाएं।',
                'स्तनपान जारी रखें, यह बीमारी से बचाता है।',
                'खाना पकाने में (जैसे दलिया या खीर में) थोड़ा गाय का दूध मिला सकते हैं, लेकिन बोतल या गिलास में भरकर पीने को न दें।'
            ];
        } else if (ageSelect === '1to2y') {
            badgeText = '✅ गाय का दूध शुरू कर सकते हैं';
            badgeClass = 'badge-green';
            title = 'गाय का दूध बेहतर (भैंस से हल्का)';
            desc = '1 साल का होने के बाद बच्चे का पाचन तंत्र मजबूत हो जाता है। अब आप उसे पशु का दूध दे सकते हैं। इस उम्र में गाय का दूध भैंस के दूध से बहुत बेहतर है। गाय के दूध में वसा (fat) कम होती है और यह पचाने में आसान होता है, साथ ही यह बच्चे के मानसिक विकास के लिए ज्यादा अच्छा माना जाता है।';
            tips = [
                'भैंस का दूध बहुत गाढ़ा होता है, जिससे बच्चे का पेट भरा रहता है और वह ठोस खाना खाना छोड़ देता है। इसलिए गाय का दूध ही चुनें।',
                'दिनभर में 400ml से ज्यादा दूध न दें, नहीं तो बच्चा खाना नहीं खाएगा और उसमें खून की कमी (Iron deficiency) हो जाएगी।',
                'दूध हमेशा बिना चीनी के देने की आदत डालें।'
            ];
        } else if (ageSelect === 'above2y') {
            badgeText = '✅ गाय या भैंस का दूध (संतुलित मात्रा)';
            badgeClass = 'badge-green';
            title = 'दोनों दूध दे सकते हैं, पर खाना है जरूरी';
            desc = '2 साल से बड़े बच्चे अब बहुत सक्रिय (active) होते हैं। आप उन्हें गाय या भैंस का दूध दे सकते हैं। अगर बच्चा कमजोर है और वजन बढ़ाना है, तो भैंस का दूध दिया जा सकता है, क्योंकि इसमें कैलोरी और वसा ज्यादा होती है। लेकिन यदि बच्चा सामान्य है, तो गाय का दूध ही सर्वोत्तम है।';
            tips = [
                'दूध को भोजन का विकल्प न बनाएं, बच्चा दाल, रोटी, सब्जी, फल सब खाए।',
                'यदि भैंस का दूध दे रहे हैं, तो मलाई निकालकर या थोड़ा पानी मिलाकर दें ताकि भारी न पड़े।',
                'हड्डियों की मजबूती के लिए दूध कैल्शियम का अच्छा स्रोत है।'
            ];
        }

        // Apply classes and content
        resultBadge.className = `result-badge ${badgeClass}`;
        resultBadge.textContent = badgeText;
        resultTitle.textContent = title;
        resultDesc.textContent = desc;

        // Render tips
        resultTipsList.innerHTML = '';
        tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            resultTipsList.appendChild(li);
        });

        // Show result box
        calcResultBox.style.display = 'block';
        
        // Smooth scroll to result
        calcResultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });

    // 5. WhatsApp Share Copy Clipboard Logic
    const btnShare = document.getElementById('btnShare');
    const shareStatus = document.getElementById('shareStatus');

    if (btnShare) {
        btnShare.addEventListener('click', () => {
            const textToCopy = `*गाय का दूध या भैंस का दूध? छोटे बच्चे के लिए क्या है सही?* 🍼
            
प्यारी मम्मी/दादी/नानी के लिए एक जरूरी संदेश:

1. *0 से 6 महीने तक:* सिर्फ और सिर्फ मां का दूध ही "अमृत" है। पानी, घुट्टी, या गाय/भैंस का दूध बिल्कुल न दें!
2. *6 से 12 महीने तक:* मां का दूध जारी रखें और ऊपर का मसला हुआ खाना शुरू करें। पीने के लिए जानवरों का दूध अभी भी मना है।
3. *1 साल के बाद:* अब दूध शुरू कर सकते हैं। लेकिन *गाय का दूध* भैंस के दूध से कहीं बेहतर है क्योंकि वह हल्का होता है और आसानी से पचता है। भैंस का दूध बहुत गाढ़ा और भारी होता है।

*डॉक्टर की सलाह:* साधारण दूध का प्रोटीन और नमक नवजात शिशु की नाजुक किडनी और आंतों को नुकसान पहुंचा सकता है।

पूरी जानकारी और बच्चे के पेट का आकार देखने के लिए नीचे दिए गए लिंक को अपने फोन में खोलें:
(यहां अपनी इस सुंदर वेबसाइट का लिंक डालें)`;

            navigator.clipboard.writeText(textToCopy).then(() => {
                shareStatus.textContent = '✅ सुंदर संदेश कॉपी हो गया है! अब इसे WhatsApp पर मम्मी को पेस्ट (Paste) करके भेजें।';
                setTimeout(() => {
                    shareStatus.textContent = '';
                }, 5000);
            }).catch(err => {
                console.error('Could not copy text: ', err);
                shareStatus.textContent = '❌ कॉपी करने में दिक्कत हुई। आप इसे मैन्युअल रूप से सिलेक्ट करके कॉपी कर सकते हैं।';
            });
        });
    }

});
