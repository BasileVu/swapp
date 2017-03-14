var STATIC_PATH = "../backend/static/public/";
var VENDOR_PATH = STATIC_PATH + "js/vendor/";

module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        src: ["node_modules/font-awesome/fonts/*"],
                        dest: STATIC_PATH + "fonts/",
                        flatten: true
                    }, {
                        expand: true,
                        src: [
                            "node_modules/tether/dist/js/tether.js",
                            "node_modules/imagesloaded/imagesloaded.pkgd.js",
                            "node_modules/jquery/dist/jquery.js",
                            "node_modules/bootstrap/dist/js/bootstrap.js",
                            "node_modules/isotope-layout/dist/isotope.pkgd.js",
                            "node_modules/flickity/dist/flickity.pkgd.js",
                            "node_modules/jquery-match-height/dist/jquery.matchHeight.js",
                            "node_modules/zone.js/dist/zone.js",
                            "node_modules/reflect-metadata/Reflect.js",
                            "node_modules/systemjs/dist/system.src.js"
                        ],
                        dest: VENDOR_PATH,
                        flatten: true
                    }, {
                        expand: true,
                        cwd: "node_modules/@angular/",
                        src: ["**"],
                        dest: VENDOR_PATH + "@angular/"
                    }, {
                        expand: true,
                        cwd: "node_modules/rxjs/",
                        src: ["**"],
                        dest: VENDOR_PATH + "rxjs/"
                    }, {
                        expand: true,
                        cwd: "node_modules/ng2-img-cropper/",
                        src: ["**"],
                        dest: VENDOR_PATH + "ng2-img-cropper/"
                    }, {
                        expand: true,
                        cwd: "node_modules/ng2-toastr/",
                        src: ["**"],
                        dest: VENDOR_PATH + "ng2-toastr/"
                    }, {
                        expand: true,
                        cwd: "node_modules/ng2-rating/",
                        src: ["**"],
                        dest: VENDOR_PATH + "ng2-rating/"
                    }
                ]
            }
        },
        sass: {
            dist: {
                files: [{ 
                    dest: STATIC_PATH + "css/styles.css", 
                    src: "scss/styles.scss" 
                }]
            }
        },
        ts: {
            default: {
                src: [STATIC_PATH + "js/app/**/*.ts", "!node_modules/**"],
                options: {
                    "target": "es5",
                    "module": "commonjs",
                    "moduleResolution": "node",
                    "sourceMap": true,
                    "emitDecoratorMetadata": true,
                    "experimentalDecorators": true,
                    "removeComments": false,
                    "noImplicitAny": false
                }
            }
        },
        watch: {
            styles: {
                files: ["scss/*.scss"],
                tasks: ["sass"]
            },
            typescripts: {
                files: [STATIC_PATH + "**/*.ts"],
                tasks: ["ts"]
            },
            livereload: {
                files : [
                    "**/templates/**/*",
                    "**/static/public/**/*",
                    "**/*.py"
                ],
                options: {
                    livereload: 8080
                }
            }
        }
    });

    grunt.loadNpmTasks("grunt-contrib-copy");
    grunt.loadNpmTasks("grunt-sync");
    grunt.loadNpmTasks("grunt-contrib-sass");
    grunt.loadNpmTasks("grunt-ts");
    grunt.loadNpmTasks("grunt-contrib-watch");

    // Default task(s).
    grunt.registerTask("default", ["copy", "sass", "ts", "watch"]);

    // Build without watch
    grunt.registerTask("build", ["copy", "sass", "ts"]);
};
