const Dashboard = ({ data }) => {
    if (!data) return <p>No data available</p>;
    const API_URL = "http://127.0.0.1:8000"; // FastAPI server
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
            <div className="grid grid-cols-3 gap-6">
                {data.map((item) => (
                    <div
                        key={item.id}
                        className="border rounded p-4 shadow hover:shadow-lg transition cursor-pointer"
                    >
                        <img
                            src={`${API_URL}/uploads/images/${item.images[0]?.filename}`}
                            alt={item.filename}
                            className="w-full h-48 object-fit rounded mb-2"
                        />
                        <h2 className="font-semibold text-lg">{item.filename}</h2>
                        <p className="text-gray-600 text-sm mt-1">
                            {item.summaries[0]?.summary || "No summary available"}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Dashboard;
