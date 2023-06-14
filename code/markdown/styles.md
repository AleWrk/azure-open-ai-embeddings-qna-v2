<style>
    [data-testid="stSidebar"] {
        width: 250px !important;
    }
    header {
        background-color: #258900 !important;
        color: white !important;
    }
    h1 {
        font-size: 1.8rem;
    }
    h2 {
        font-size: 1.2rem;
        padding-bottom: 30px;
    }
    [data-testid="stHeader"] {
        background-image: url("data:image/png;base64,{img-isp}");
        background-repeat: no-repeat;
        background-size: 150px;
        background-position: 270px 15px;
    }
    [data-testid="stSidebarNav"] {
        background-image: url("data:image/png;base64,{img-isl}");
        background-repeat: no-repeat;
        background-size: 150px;
        padding-top: 190px;
        background-position: 45px 0px;
    } 
    [data-testid="stSidebarNav"]::before {
        content: "{title}";
        top:230px;
        left: 50%;
        transform: translate(-50%, -25px);
        position: absolute;
        white-space: pre;
        display: inline;
        font-weight: bolder;
        font-size: 1.6rem;
        border-bottom: 1px solid #ccc;
    }        
    footer {	
	    visibility: hidden;	
	}
    footer:after {
        content:'Innovazione Sperimentazioni & Lab'; 
        visibility: visible;
        display: block;
        position: relative;
        padding: 5px;
        top: 2px;
    }
    [data-testid="stHorizontalBlock"] button {
        background-color: #258900 !important;
        color: white !important;
        font-weight: bolder;
        width: 100%;
        position: relative;
        bottom: 0;
        top: 33px;
    }
    
</style>