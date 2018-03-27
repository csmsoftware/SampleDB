

function display_samples(target_selector,samples,clickable){

    html = "";

    for(i=0;i<samples.length;i++){

        sample = samples[i];

        //console.log(sample)

        if (clickable){
            html = html + '<tr class="clickable-row" id="s-' + sample.pk + '">';
        } else{
            html = html + '<tr id="s-' + sample.pk + '">';
        }

        html = html + '<td class="sample-pk">' + sample.pk + '</td>';

        html = html + '<td id="study_title-' + sample.pk + '">' + ((sample.fields.study_title != null) ? sample.fields.study_title : "" ) + '</td>';
        html = html + '<td id="sample_id-' + sample.pk + '">' + ((sample.fields.sample_id != null) ? sample.fields.sample_id : "" ) + '</td>';
        html = html + '<td id="species-' + sample.pk + '">' + ((sample.fields.species != null) ? sample.fields.species : "" ) + '</td>';
        html = html + '<td id="sample_storage_type-' + sample.pk + '">' + ((sample.fields.sample_storage_type != null) ? sample.fields.sample_storage_type : "" ) + '</td>';
        html = html + '<td id="sample_matrix-' + sample.pk + '">' + ((sample.fields.sample_matrix != null) ? sample.fields.sample_matrix : "" ) + '</td>';
        html = html + '<td id="collection_protocol-' + sample.pk + '">' + ((sample.fields.collection_protocol != null) ? sample.fields.collection_protocol : "" ) + '</td>';
        html = html + '<td id="campus-' + sample.pk + '">' + ((sample.fields.campus != null) ? sample.fields.campus : "" ) + '</td>';
        html = html + '<td id="building-' + sample.pk + '">' + ((sample.fields.building != null) ? sample.fields.building : "" ) + '</td>';
        html = html + '<td id="room-' + sample.pk + '">' + ((sample.fields.room != null) ? sample.fields.room : "" ) + '</td>';
        html = html + '<td id="freezer_id-' + sample.pk + '">' + ((sample.fields.freezer_id != null) ? sample.fields.freezer_id : "" ) + '</td>';
        html = html + '<td id="shelf_id-' + sample.pk + '">' + ((sample.fields.shelf_id != null) ? sample.fields.shelf_id : "" ) + '</td>';
        html = html + '<td id="box_id-' + sample.pk + '">' + ((sample.fields.box_id != null) ? sample.fields.box_id : "" ) + '</td>';
        html = html + '<td id="parent_type-' + sample.pk + '">' + ((sample.fields.parent_type != null) ? sample.fields.parent_type : "" ) + '</td>';
        html = html + '<td id="parent_id-' + sample.pk + '">' + ((sample.fields.parent_id != null) ? sample.fields.parent_id : "" ) + '</td>';
        html = html + '<td id="consent_form_information-' + sample.pk + '">' + ((sample.fields.consent_form_information != null) ? sample.fields.consent_form_information : "" ) + '</td>';
        html = html + '<td id="tissue_bank_reference-' + sample.pk + '">' + ((sample.fields.tissue_bank_reference != null) ? sample.fields.tissue_bank_reference : "" ) + '</td>';
        html = html + '<td id="hazard_group-' + sample.pk + '">' + ((sample.fields.hazard_group != null) ? sample.fields.hazard_group : "" ) + '</td>';
        html = html + '<td id="hazard_description-' + sample.pk + '">' + ((sample.fields.hazard_description != null) ? sample.fields.hazard_description : "" ) + '</td>';
        html = html + '<td id="datetime_created-' + sample.pk + '">' + sample.fields.datetime_created + '</td>';
        html = html + '</tr>';

    }

//    $('#sample-table-body').html(html);

    $(target_selector).html(html);


}


