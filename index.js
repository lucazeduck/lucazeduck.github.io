
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Monke Mod Manager</title>

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial, Helvetica, sans-serif;
}

body{
    background:#0d0d0d;
    color:#d8d8d8;
    display:flex;
    height:100vh;
    overflow:hidden;
}

.sidebar{
    width:230px;
    background:#111111;
    border-right:1px solid #1d1d1d;
    padding:15px;
    display:flex;
    flex-direction:column;
    gap:10px;
}

.logo{
    font-size:28px;
    font-weight:bold;
    margin-bottom:20px;
    color:#ffffff;
}

.nav-top{
    flex:1;
}

.nav-btn{
    width:100%;
    background:#181818;
    border:1px solid #2a2a2a;
    color:#d8d8d8;
    padding:14px;
    margin-bottom:10px;
    text-align:left;
    border-radius:6px;
    cursor:pointer;
    transition:0.15s;
    font-size:15px;
}

.nav-btn:hover{
    background:#242424;
    border-color:#555;
    transform:translateX(3px);
}

.bottom-buttons{
    margin-top:auto;
}

.content{
    flex:1;
    padding:18px;
    overflow:auto;
}

.section{
    display:none;
}

.section.active{
    display:block;
}

.category-title{
    color:#ffffff;
    margin-bottom:10px;
    font-size:22px;
}

.table{
    width:100%;
    border-collapse:collapse;
    background:#111111;
    border:1px solid #1f1f1f;
}

.table tr{
    border-bottom:1px solid #1b1b1b;
}

.table tr:hover{
    background:#1a1a1a;
}

.table td{
    padding:10px;
    font-size:15px;
}

.link-box{
    width:18px;
    height:18px;
    background:white;
    border:none;
    cursor:pointer;
    transition:0.15s;
}

.link-box:hover{
    transform:scale(1.15);
    background:#cfcfcf;
}

.placeholder{
    margin-top:20px;
    background:#161616;
    border:1px dashed #555;
    padding:25px;
    border-radius:8px;
    text-align:center;
    color:#bdbdbd;
    font-size:18px;
}

@media (max-width:768px){

body{
    flex-direction:column;
    overflow:auto;
}

.sidebar{
    width:100%;
    flex-direction:row;
    overflow-x:auto;
    border-right:none;
    border-bottom:1px solid #1d1d1d;
    padding:10px;
}

.logo{
    display:none;
}

.nav-top,
.bottom-buttons{
    display:flex;
    flex-direction:row;
    gap:8px;
    margin:0;
}

.nav-btn{
    min-width:120px;
    padding:10px;
    font-size:13px;
    margin-bottom:0;
    white-space:nowrap;
}

.content{
    padding:12px;
}

.table td{
    font-size:13px;
    padding:8px;
}

.link-box{
    width:22px;
    height:22px;
}

.category-title{
    font-size:18px;
}
}

</style>
</head>

<body>

<div class="sidebar">

    <div class="logo">Monke Mod Manager</div>

    <div class="nav-top">

        <button class="nav-btn" onclick="showSection('core')">Core</button>
        <button class="nav-btn" onclick="showSection('gameplay')">Gameplay</button>
        <button class="nav-btn" onclick="showSection('tweaks')">Tweaks / Tools</button>
        <button class="nav-btn" onclick="showSection('menus')">Menus</button>
        <button class="nav-btn" onclick="showSection('mymods')">My Mods</button>

    </div>

    <div class="bottom-buttons">

        <button class="nav-btn" onclick="showSection('credits')">credits</button>
        <button class="nav-btn" onclick="showSection('info')">Info</button>
        <button class="nav-btn" onclick="window.open('https://github.com/AltAchiever1', '_blank')">GitHub</button>
        <button class="nav-btn" onclick="window.open('https://discord.gg/wP55pJSR2W', '_blank')">Discord</button>

    </div>

</div>

<div class="content">

    <div class="section active" id="core">
        <div class="category-title">Core</div>
        <table class="table">
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/BepInEx/BepInEx/releases/latest','_blank')"></button></td>
                <td>BepInEx - 5.4.23.5</td>
                <td>BepInEx Team</td>
            </tr>
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/Seralyth/Utilla/releases/latest','_blank')"></button></td>
                <td>Utilla - 1.8.0 {B}</td>
                <td>Seralyth</td>
            </tr>
        </table>
    </div>

    <div class="section" id="gameplay">
        <div class="category-title">Gameplay</div>
        <div class="placeholder">I Dont Have Anything To Put Here Yet</div>
    </div>

    <div class="section" id="tweaks">
        <div class="category-title">Tweaks / Tools</div>
        <table class="table">
            <tr>
                <td><button class="link-box" onclick="window.open('https://codeberg.org/notabird/Overstocked/releases/latest','_blank')"></button></td>
                <td>OverStocked - 1.2.1</td>
                <td>Not A Bird</td>
            </tr>
        </table>
    </div>

    <div class="section" id="menus">
        <div class="category-title">Menus</div>
        <table class="table">
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/Seralyth/Seralyth-Menu/releases/latest','_blank')"></button></td>
                <td>Seralyth</td>
                <td>King of Netflix</td>
            </tr>
        </table>
    </div>

    <div class="section" id="mymods">
        <div class="category-title">My Mods</div>
        <table class="table">
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/AltAchiever1/Water-Sound-Tweaks/releases/latest','_blank')"></button></td>
                <td>Water Sound Tweaks</td>
                <td>AltAchiever</td>
            </tr>
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/AltAchiever1/Simply-Windowed/releases/latest','_blank')"></button></td>
                <td>Simply Windowed</td>
                <td>AltAchiever</td>
            </tr>
        </table>
    </div>

    <div class="section" id="credits">
        <div class="category-title">Credits</div>
        <table class="table">
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/AltAchiever1','_blank')"></button></td>
                <td>AltAchiever/Sleepyhead</td>
                <td>Me 👍</td>
            </tr>
            <tr>
                <td><button class="link-box" onclick="window.open('https://codeberg.org/notabird','_blank')"></button></td>
                <td>Not A Bird</td>
                <td></td>
            </tr>
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/kingofnetflix','_blank')"></button></td>
                <td>King of Netflix</td>
                <td></td>
            </tr>
            <tr>
                <td><button class="link-box" onclick="window.open('https://github.com/BepInEx','_blank')"></button></td>
                <td>BepInEx Team</td>
                <td>Just using The Team Because Too many People</td>
            </tr>
        </table>
    </div>

    <div class="section" id="info">
        <div class="category-title">Info</div>
        <p>Some people are new to modding and don’t know how to install or find working mods, so I made this to provide an easier way to discover and download them. I also tried to recreate the look of MMM while still keeping it a bit original. Sorry if it’s not perfect I’m horrendously bad at HTML.

If you want any mods added, make a ticket or suggestion in the Discord. If enough people ask, I’ll also add MelonLoader support and a tutorial page explaining how to use the different platforms.</p>
    </div>

</div>

<script>
function showSection(id){
document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
document.getElementById(id).classList.add('active');
}
</script>

</body>
</html>
