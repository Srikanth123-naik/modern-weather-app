document.addEventListener("DOMContentLoaded", () => {

    const weatherMain = document.getElementById("weather-main");

    function setBackground(weather) {

        weather = weather.toLowerCase();

        if (weather.includes("cloud")) {
            document.body.style.background =
            "url('https://images.unsplash.com/photo-1534088568595-a066f410bcda?q=80&w=1974&auto=format&fit=crop') center/cover no-repeat fixed";
        }

        else if (weather.includes("rain")) {
            document.body.style.background =
            "url('https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?q=80&w=1974&auto=format&fit=crop') center/cover no-repeat fixed";
        }

        else if (weather.includes("clear")) {
            const hour = new Date().getHours();

            if(hour >= 6 && hour < 18){
                document.body.style.background =
                "url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1974&auto=format&fit=crop') center/cover no-repeat fixed";
            }
            else{
                document.body.style.background =
                "url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1974&auto=format&fit=crop') center/cover no-repeat fixed";
            }
        }

        else if (weather.includes("mist") || weather.includes("fog")) {
            document.body.style.background =
            "url('https://images.unsplash.com/photo-1485236715568-ddc5ee6ca227?q=80&w=1974&auto=format&fit=crop') center/cover no-repeat fixed";
        }

        else {
            document.body.style.background =
            "linear-gradient(to right, #141e30, #243b55)";
        }
    }

    if(weatherMain){
        setBackground(weatherMain.innerText);
    }

});