<section id="local">
    <script>
        var latitude = {instituicao[latitude]}
        var longitude = {instituicao[longitude]}
    </script>
    <div class="container">
        <h2 class="subtitle">Local</h2>
        <p>
            {instituicao[long_name]}<br/>
            {instituicao[endereco]}<br/>
            {cidade} - Rio Grande do Sul
        </p>
        <div id="map_canvas" style="width: 100%; height: 350px;"></div>
        <input type="text" id="search-route" class="form-control" placeholder="Digite sua localiza&ccedil;&atilde;o">
        <div id="directions-panel"></div>
        {local_map}
    </div>
</section>
