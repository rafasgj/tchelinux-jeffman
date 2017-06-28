<section id="local">
    <script>
        var latitude = {institution[latitude]}
        var longitude = {institution[longitude]}
    </script>
    <div class="container">
        <h2 class="subtitle">Local</h2>
        <p>
            {institution[long_name]}<br/>
            {institution[address]}<br/>
            {city} - Rio Grande do Sul
        </p>
        <div id="map_canvas" style="width: 100%; height: 350px;"></div>
        <input type="text" id="search-route" class="form-control" placeholder="Digite sua localiza&ccedil;&atilde;o">
        <div id="directions-panel"></div>
        {local_map}
    </div>
</section>
