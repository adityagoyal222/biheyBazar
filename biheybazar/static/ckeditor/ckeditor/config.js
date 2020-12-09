/**
 * @license Copyright (c) 2003-2020, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.uiColor= '#FFFFFF';
	config.width = 100;     // 500 pixels wide.
	config.width = '15%'; 
	config.font_defaultLabel = 'Arial';
	config.fontSize_defaultLabel = '30';
};


CKEDITOR.on( 'instanceReady', function( ev ) {
	ev.editor.setData('<span style="font-family:Arial, Verdana, sans-serif;">&shy;</span>');
});

// CKEDITOR.config.font_default = 'Arial';
// CKEDITOR.config.fontSize_default = '20'; 