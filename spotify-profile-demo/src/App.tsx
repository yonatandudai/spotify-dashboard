import { useState, useEffect } from 'react'
import './App.css'

interface SpotifyUser {
  id: string
  display_name: string
  email: string
  images: Array<{ url: string }>
  external_urls: { spotify: string }
  uri: string
  followers: { total: number }
}

interface SpotifyTrack {
  name: string
  artists: Array<{ name: string }>
  album: { name: string, images: Array<{ url: string }> }
  external_urls: { spotify: string }
  popularity: number  // Spotify's popularity score (0-100)
  duration_ms: number
}

interface SpotifyArtist {
  name: string
  genres: string[]
  popularity: number
  followers: { total: number }
  images: Array<{ url: string }>
  external_urls: { spotify: string }
}

function App() {
  const [user, setUser] = useState<SpotifyUser | null>(null)
  const [topTracks, setTopTracks] = useState<SpotifyTrack[]>([])
  const [topArtists, setTopArtists] = useState<SpotifyArtist[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [timeRange, setTimeRange] = useState<'short_term' | 'medium_term' | 'long_term'>('medium_term')
  const [artistsTimeRange, setArtistsTimeRange] = useState<'short_term' | 'medium_term' | 'long_term'>('medium_term')
  const [showRawData, setShowRawData] = useState(false)
  const [rawUserData, setRawUserData] = useState<any>(null)
  const [rawTracksData, setRawTracksData] = useState<any>(null)
  const [rawArtistsData, setRawArtistsData] = useState<any>(null)

  const handleLogin = async () => {
    try {
      window.location.href = '/api/auth/login'
    } catch (err) {
      setError('Failed to initiate login')
    }
  }

  const fetchUserData = async (tracksTimeRange?: string, artistsTimeRange?: string) => {
    setLoading(true)
    setError(null)
    
    // Use provided parameters or fall back to state values
    const actualTracksTimeRange = tracksTimeRange || timeRange
    const actualArtistsTimeRange = artistsTimeRange || artistsTimeRange
    
    console.log('🎵 Fetching data with time ranges:', { 
      tracks: actualTracksTimeRange, 
      artists: actualArtistsTimeRange 
    })
    
    try {
      // Fetch user profile
      const userResponse = await fetch('/api/user/profile', {
        credentials: 'include' // Include cookies in the request
      })
      if (!userResponse.ok) throw new Error('Failed to fetch user profile')
      const userData = await userResponse.json()
      setUser(userData)
      setRawUserData(userData) // Store raw user data

      // Fetch top tracks
      const tracksResponse = await fetch(`/api/user/top-tracks?time_range=${actualTracksTimeRange}&limit=50`, {
        credentials: 'include' // Include cookies in the request
      })
      if (!tracksResponse.ok) throw new Error('Failed to fetch top tracks')
      const tracksData = await tracksResponse.json()
      console.log('📊 Tracks data for', actualTracksTimeRange, ':', tracksData.items?.slice(0,3).map((t: any) => t.name))
      setTopTracks(tracksData.items || [])
      setRawTracksData(tracksData) // Store raw tracks data

      // Fetch top artists
      const artistsResponse = await fetch(`/api/user/top-artists?time_range=${actualArtistsTimeRange}&limit=50`, {
        credentials: 'include' // Include cookies in the request
      })
      if (!artistsResponse.ok) throw new Error('Failed to fetch top artists')
      const artistsData = await artistsResponse.json()
      console.log('🎤 Artists data for', actualArtistsTimeRange, ':', artistsData.items?.slice(0,3).map((a: any) => a.name))
      setTopArtists(artistsData.items || [])
      setRawArtistsData(artistsData) // Store raw artists data
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { 
        method: 'POST',
        credentials: 'include' // Include cookies in the request
      })
      setUser(null)
      setTopTracks([])
    } catch (err) {
      setError('Failed to logout')
    }
  }

  // Check if user is already logged in on component mount
  useEffect(() => {
    const checkAuth = async () => {
      // Check if we just completed OAuth
      const urlParams = new URLSearchParams(window.location.search)
      const authComplete = urlParams.get('auth_complete')
      const sessionId = urlParams.get('session_id')
      
      if (authComplete === 'true' && sessionId) {
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname)
        
        // Set the session cookie manually
        document.cookie = `session_id=${sessionId}; path=/; max-age=3600; SameSite=Lax`
        
        // Wait a moment then try to fetch data
        setTimeout(async () => {
          try {
            const response = await fetch('/api/user/profile', {
              credentials: 'include'
            })
            if (response.ok) {
              fetchUserData()
            } else {
              console.log('Still not authenticated after OAuth, status:', response.status)
            }
          } catch (err) {
            console.log('Error after OAuth:', err)
          }
        }, 500) // Wait 0.5 seconds
        return
      }
      
      // Normal auth check
      try {
        const response = await fetch('/api/user/profile', {
          credentials: 'include' // Include cookies in the request
        })
        if (response.ok) {
          fetchUserData()
        }
      } catch (err) {
        // User not logged in, which is fine
      }
    }
    
    checkAuth()
  }, [])

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎵 Spotify Profile Demo</h1>
        
        {!user ? (
          <div className="login-section">
            <p>Connect your Spotify account to see your profile and top tracks</p>
            <button onClick={handleLogin} className="login-btn">
              Login with Spotify
            </button>
          </div>
        ) : (
          <div className="user-section">
            <div className="user-profile">
              <div className="profile-info">
                {user.images && user.images[0] && (
                  <img 
                    src={user.images[0].url} 
                    alt="Profile" 
                    className="profile-image"
                  />
                )}
                <div className="profile-details">
                  <h2>Welcome, {user.display_name}!</h2>
                  <p><strong>User ID:</strong> {user.id}</p>
                  <p><strong>Email:</strong> {user.email}</p>
                  <p><strong>Followers:</strong> {user.followers?.total || 0}</p>
                  <p>
                    <strong>Spotify Profile:</strong>{' '}
                    <a 
                      href={user.external_urls.spotify} 
                      target="_blank" 
                      rel="noopener noreferrer"
                    >
                      View on Spotify
                    </a>
                  </p>
                </div>
              </div>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>

            <div className="top-tracks-section">
              <h3>Your Top 50 Tracks</h3>
              
              <div className="controls">
                <div className="time-range-selector">
                  <label htmlFor="timeRange">Time Range: </label>
                  <select 
                    id="timeRange"
                    value={timeRange} 
                    onChange={(e) => {
                      const newTimeRange = e.target.value as 'short_term' | 'medium_term' | 'long_term'
                      setTimeRange(newTimeRange)
                      // Auto-refresh when time range changes
                      setTimeout(() => fetchUserData(newTimeRange, artistsTimeRange), 100)
                    }}
                  >
                    <option value="short_term">🕐 Last 4 Weeks (Recent trends)</option>
                    <option value="medium_term">📅 Last 6 Months (Seasonal patterns)</option>
                    <option value="long_term">📈 All Time (Complete history)</option>
                  </select>
                </div>
                
                <div className="debug-controls">
                  <label>
                    <input 
                      type="checkbox" 
                      checked={showRawData} 
                      onChange={(e) => setShowRawData(e.target.checked)}
                    />
                    Show Raw API Data
                  </label>
                </div>
                
                <button onClick={() => fetchUserData()} className="refresh-btn" disabled={loading}>
                  {loading ? 'Loading...' : 'Refresh Data'}
                </button>
              </div>
              
              {topTracks.length > 0 ? (
                <div className="tracks-grid">
                  {topTracks.map((track, index) => (
                    <div key={index} className="track-card">
                      <div className="track-rank">#{index + 1}</div>
                      {track.album.images[0] && (
                        <img 
                          src={track.album.images[0].url} 
                          alt={track.album.name}
                          className="track-image"
                        />
                      )}
                      <div className="track-info">
                        <h4>{track.name}</h4>
                        <p>{track.artists.map(artist => artist.name).join(', ')}</p>
                        <p className="album-name">{track.album.name}</p>
                        <div className="track-stats">
                          <span className="popularity">Popularity: {track.popularity}%</span>
                          <span className="duration">{Math.floor(track.duration_ms / 60000)}:{String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}</span>
                        </div>
                        <a 
                          href={track.external_urls.spotify} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="spotify-link"
                        >
                          Play on Spotify
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No top tracks found. Try refreshing!</p>
              )}
            </div>

            <div className="top-artists-section">
              <div className="section-header">
                <h3>🎤 Your Top 50 Artists</h3>
                <div className="section-subtitle">
                  Discover your musical journey through data-driven insights
                </div>
                
                {/* Artists-specific time range selector */}
                <div className="artists-time-selector">
                  <label htmlFor="artistsTimeRange">📅 Artists Time Range: </label>
                  <select 
                    id="artistsTimeRange"
                    value={artistsTimeRange} 
                    onChange={(e) => {
                      const newArtistsTimeRange = e.target.value as 'short_term' | 'medium_term' | 'long_term'
                      setArtistsTimeRange(newArtistsTimeRange)
                      // Auto-refresh artists data when time range changes
                      setTimeout(() => fetchUserData(timeRange, newArtistsTimeRange), 100)
                    }}
                    className="enhanced-selector"
                  >
                    <option value="short_term">🕐 Last 4 Weeks - Recent Obsessions</option>
                    <option value="medium_term">📅 Last 6 Months - Seasonal Favorites</option>
                    <option value="long_term">📈 All Time - Core Musical DNA</option>
                  </select>
                </div>
              </div>
            <div className="ranking-explanation">
              <h4>How Rankings Work:</h4>
              <div className="time-range-details">
                <strong>Current Artists Time Range: {
                  artistsTimeRange === 'short_term' ? 'Last 4 Weeks (Recent Obsessions)' : 
                  artistsTimeRange === 'medium_term' ? 'Last 6 Months (Seasonal Favorites)' : 
                  'All Time (Core Musical DNA)'
                }</strong>
              </div>
              <ul>
                <li><strong>Position #{"{"}1-50{"}"}</strong> = Your most to least listened artists in the selected time period</li>
                <li><strong>Data Source</strong> = Based on your actual Spotify listening history</li>
                <li><strong>Ranking Logic</strong> = Total time you've spent listening to each artist's songs</li>
                <li><strong>Update Frequency</strong> = Spotify updates this data daily</li>
                <li><strong>Privacy Note</strong> = Spotify provides rankings but not exact play counts or minutes listened</li>
              </ul>
              <div className="time-range-comparison">
                <p><strong>Time Range Comparison:</strong></p>
                <ul>
                  <li><strong>Short Term (4 weeks)</strong> = Recent listening habits, current favorites</li>
                  <li><strong>Medium Term (6 months)</strong> = Seasonal patterns, recent discoveries</li>
                  <li><strong>Long Term (All time)</strong> = Overall music taste, long-standing favorites</li>
                </ul>
              </div>
            </div>              {topArtists.length > 0 ? (
                <div>
                  {/* Summary Stats */}
                  <div className="artist-summary">
                    <h4>Your Music Profile Summary:</h4>
                    <div className="current-period">
                      <strong>Analyzing: {
                        artistsTimeRange === 'short_term' ? 'Last 4 Weeks (Recent Trends)' : 
                        artistsTimeRange === 'medium_term' ? 'Last 6 Months (Medium-term Patterns)' : 
                        'All Time (Complete History)'
                      }</strong>
                    </div>
                    <div className="summary-stats">
                      <div className="summary-item">
                        <span className="summary-label">Total Top Artists:</span>
                        <span className="summary-value">{topArtists.length}</span>
                      </div>
                      <div className="summary-item">
                        <span className="summary-label">Most Popular Artist:</span>
                        <span className="summary-value">{topArtists[0]?.name} (#{1})</span>
                      </div>
                      <div className="summary-item">
                        <span className="summary-label">Highest Global Popularity:</span>
                        <span className="summary-value">{Math.max(...topArtists.map(a => a.popularity))}% ({topArtists.find(a => a.popularity === Math.max(...topArtists.map(a => a.popularity)))?.name})</span>
                      </div>
                      <div className="summary-item">
                        <span className="summary-label">Most Common Genres:</span>
                        <span className="summary-value">{
                          (() => {
                            const genreCounts = topArtists.flatMap(a => a.genres)
                              .reduce((acc, genre) => {
                                acc[genre] = (acc[genre] || 0) + 1;
                                return acc;
                              }, {} as Record<string, number>);
                            
                            return Object.entries(genreCounts)
                              .sort((a, b) => b[1] - a[1])
                              .slice(0, 3)
                              .map(([genre]) => genre)
                              .join(', ');
                          })()
                        }</span>
                      </div>
                    </div>
                  </div>

                  <div className="artists-grid">
                  {topArtists.map((artist, index) => (
                    <div key={index} className="artist-card enhanced">
                      <div className="artist-rank-badge">
                        <span className="rank-number">#{index + 1}</span>
                        <span className="rank-tier">
                          {index === 0 ? '👑 TOP' : index < 3 ? '⭐ HIGH' : index < 10 ? '📈 MID' : '📊 LOW'}
                        </span>
                      </div>
                      
                      <div className="artist-image-container">
                        {artist.images[0] && (
                          <img 
                            src={artist.images[0].url} 
                            alt={artist.name}
                            className="artist-image"
                          />
                        )}
                        <div className="popularity-overlay">
                          <span className="popularity-score">{artist.popularity}%</span>
                          <span className="popularity-label">Global</span>
                        </div>
                      </div>
                      
                      <div className="artist-info enhanced">
                        <h4 className="artist-name">{artist.name}</h4>
                        
                        {artist.genres.length > 0 && (
                          <div className="genres-container">
                            <div className="genres-label">🎭 Genres:</div>
                            <div className="genres-list">
                              {artist.genres.slice(0, 4).map((genre, i) => (
                                <span key={i} className="genre-tag">{genre}</span>
                              ))}
                              {artist.genres.length > 4 && (
                                <span className="genre-tag more">+{artist.genres.length - 4} more</span>
                              )}
                            </div>
                          </div>
                        )}
                        
                        <div className="artist-stats enhanced">
                          <div className="stat-row primary">
                            <div className="stat-item">
                              <span className="stat-icon">📊</span>
                              <div className="stat-content">
                                <span className="stat-label">Your Ranking</span>
                                <span className="stat-value">#{index + 1} of 50</span>
                              </div>
                            </div>
                            <div className="stat-item">
                              <span className="stat-icon">👥</span>
                              <div className="stat-content">
                                <span className="stat-label">Followers</span>
                                <span className="stat-value">{(artist.followers.total / 1000000).toFixed(1)}M</span>
                              </div>
                            </div>
                          </div>
                          
                          <div className="stat-row secondary">
                            <div className="listening-context">
                              <span className="context-icon">⏱️</span>
                              <span className="context-text">
                                {artistsTimeRange === 'short_term' ? 'Recent favorite' : 
                                 artistsTimeRange === 'medium_term' ? 'Seasonal preference' : 
                                 'Long-term favorite'} 
                                ({artistsTimeRange.replace('_', ' ')})
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        <div className="artist-actions">
                          <a 
                            href={artist.external_urls.spotify} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="spotify-link enhanced"
                          >
                            <span className="link-icon">🎵</span>
                            View on Spotify
                          </a>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                </div>
              ) : (
                <p>No top artists found. Try refreshing!</p>
              )}
            </div>
          </div>
        )}

        {/* Raw Data Debug Section */}
        {showRawData && (rawUserData || rawTracksData || rawArtistsData) && (
          <div className="raw-data-section">
            <h3>Raw API Data</h3>
            
            {rawUserData && (
              <div className="raw-data-block">
                <h4>User Profile Response:</h4>
                <pre className="raw-data">
                  {JSON.stringify(rawUserData, null, 2)}
                </pre>
              </div>
            )}
            
            {rawTracksData && (
              <div className="raw-data-block">
                <h4>Top Tracks Response (Time Range: {timeRange}):</h4>
                <pre className="raw-data">
                  {JSON.stringify(rawTracksData, null, 2)}
                </pre>
              </div>
            )}

            {rawArtistsData && (
              <div className="raw-data-block">
                <h4>Top Artists Response (Time Range: {artistsTimeRange}):</h4>
                <pre className="raw-data">
                  {JSON.stringify(rawArtistsData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>Error: {error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}
      </header>
    </div>
  )
}

export default App
