import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';

// Set worker URL to load PDF.js worker from local public folder
pdfjs.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

const PdfThumbnail = ({ pdfPath, altTitle }) => {
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
        setLoading(false);
    }

    function onDocumentLoadError(err) {
        console.error("PDF Load Error:", err);
        setError(true);
        setLoading(false);
    }

    return (
        <div className="w-full h-full relative overflow-hidden bg-gray-100 flex items-center justify-center">
            {loading && !error && (
                <div className="absolute inset-0 flex items-center justify-center z-10 bg-gray-100">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-brand-sage"></div>
                </div>
            )}

            {error ? (
                <div className="flex flex-col items-center justify-center text-brand-sage/50 p-4 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="text-xs uppercase tracking-wider">PDF</span>
                </div>
            ) : (
                <Document
                    file={pdfPath}
                    onLoadSuccess={onDocumentLoadSuccess}
                    onLoadError={onDocumentLoadError}
                    loading={<div></div>}
                    className="w-full h-full flex items-center justify-center"
                >
                    <Page
                        pageNumber={1}
                        width={200} // Render at a reasonable width for thumbnail
                        renderTextLayer={false}
                        renderAnnotationLayer={false}
                        className="shadow-sm"
                    />
                </Document>
            )}
        </div>
    );
};

export default PdfThumbnail;
