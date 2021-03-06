
'use strict';

const gulp = require('gulp');
const size = require('gulp-size');
const clean = require('gulp-clean');
const babel = require('gulp-babel');

gulp.task(
    'transform', () => {
        gulp.src('project/static/src/*.js')
            .pipe(
                babel({
                    presets: ['es2015', 'react', 'stage-0'],
					"plugins": ["transform-flow-strip-types"]
                }))
            .pipe(gulp.dest('project/static/dist'))
            .pipe(size())
    }
);

gulp.task('clean', () => {
    gulp.src('project/static/dist/*.js', {read: false})
        .pipe(clean());
});

gulp.task(
    'default', ['clean'], () => {
        gulp.start('transform');
    }
);
