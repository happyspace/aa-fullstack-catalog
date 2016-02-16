
'use strict';

const gulp = require('gulp');
const size = require('gulp-size');
const babel = require('gulp-babel');

gulp.task(
    'transform', () => {
        gulp.src('project/static/src/*.js')
            .pipe(
                babel({
                    presets: ['es2015', 'react', 'stage-0']
                }))
            .pipe(gulp.dest('project/static/build'))
            .pipe(size())
    }
);

gulp.task(
    'default', () => {
        console.log("hello!")
    }
);
