import React, { Component } from 'react';
import { connect } from 'react-redux';

import PlayItemsPage from '../components/playitem/PlayItemsPage';
import FlashMessage from '../components/FlashMessage';

import Header from '../components/Header'
import Footer from '../components/Footer'

import Filters from '../components/filter/Filters';
import InputFilter from '../components/filter/InputFilter';

import { playitemActions, playlistActions } from '../actions';
import Pagination from '../components/Pagination';

import '../stylesheets/Pagination.css'


class Home extends Component {

    state = {
        filters: {
            title: ''
        },
        allCountries: [],
        currentCountries: [],
        currentPage: null,
        totalPages: null
    }


    onPageChanged = data => {
        //const { allCountries } = this.state;
        const { currentPage, totalPages, pageLimit } = data;



        const filters = {
            pageNum: data.currentPage,

            pageSize: data.pageLimit
        }

        //console.log(JSON.stringify(filters))
        this.props.dispatch(playitemActions.fetchPlayItems(filters));

    }

    onFilterChange = (filters) => {
        console.log(filters)
        this.setState({
            filters
        });
    }


    componentDidMount() {
        const filters = {
            pageNum: this.props.pagination.current_page,

            pageSize: this.props.pagination.page_size
        }
        //this.props.dispatch(playitemActions.fetchPlayItems(filters));


        this.props.dispatch(playlistActions.fetchPlaylists());
    }

    onCreatePlayItem = ({title, description}) => {
        this.props.dispatch(playitemActions.createPlayItem({
            title,
            description
        }));
    };

    onStatusChange = (id, status) => {
        this.props.dispatch(playitemActions.editPlayItem(id, {
            status
        }));
    };

    render() {

        //console.log('home render')

        //const { allCountries, currentCountries, currentPage, totalPages } = this.state;
        //const totalCountries = allCountries.length;
        //
        //if (totalCountries === 0) return null;
        //
        //const {filters} = this.state;
        //const { pagination }= this.props

        //
        const headerClass = ['text-dark py-2 pr-4 m-0', this.props.pagination.current_page ? 'border-gray border-right' : ''].join(' ').trim();

        const total_pages = ~~((this.props.pagination.total_count + this.props.pagination.page_size - 1 )/this.props.pagination.page_size)

        // console.log(this.props.pagination.total_count)

        return (

            <div>
                <Header />
                { this.props.error && <FlashMessage message={ this.props.error } /> }
                <div className="main-content">
                    <PlayItemsPage playitems={ this.props.playitems }
                        onCreatePlayItem={ this.onCreatePlayItem }
                        onStatusChange={ this.onStatusChange }
                        isLoading={ this.props.isLoading } />

                    <div className="w-100 px-4 py-5 d-flex flex-row flex-wrap align-items-center justify-content-between">
                        <div className="d-flex flex-row align-items-center">
                            <h2 className={ headerClass }><strong className="text-secondary">{ this.props.pagination.total_count }</strong> 播放地址</h2>
                            {  this.props.pagination.current_page && (
                                <span className="current-page d-inline-block h-100 pl-4 text-secondary"> <span className="font-weight-bold">第 { this.props.pagination.current_page } 页</span> / <span className="font-weight-bold">共 { total_pages } 页</span></span>
                            ) }
                        </div>
                        <div className="d-flex flex-row py-4 align-items-center">
                            <Pagination totalRecords={ this.props.pagination.total_count }
                                        pageLimit={ this.props.pagination.page_size }
                                        pageNeighbours={ 2 }
                                        onPageChanged={ this.onPageChanged } />
                        </div>
                    </div>

                </div>
                <Footer />
            </div>
            );
    }
}

function mapStateToProps(state) {
    const {pagination, playitems, isLoading, error} = state.playitems;

    const {playlists} = state.playlists;

    return {
        pagination,
        playitems,
        isLoading,
        error,
        playlists
    };
}

export default connect(mapStateToProps)(Home);